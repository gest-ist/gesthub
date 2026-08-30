#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.14"
# dependencies = ["flask>=3.1,<4", "python-dotenv>=1.2,<2", "waitress>=3,<4"]
# ///
"""Pull the repository and build its images when GitHub sends a webhook.

Setup
-----
Add at least this setting to the repository's ``.env`` file::

    SYNC_WEBHOOK_SECRET=replace-with-a-long-random-value

The optional settings are ``SYNC_WEBHOOK_PATH`` (default ``/sync``),
``SYNC_REMOTE`` (``origin``), ``SYNC_BRANCH`` (``main``), and ``GEST_IMAGE``
(``gest-website``). If the path changes, Caddy reads the same setting.

Install and immediately start the checked-in user service from the repository root::

    systemctl --user enable --now "$PWD/scripts/git-sync.service"

The service creates ``.git-sync/webhook.sock`` automatically. Then start the Compose
stack, which mounts that directory into Caddy::

    docker compose up -d

Configure a GitHub webhook for ``https://<domain>/<path>`` with JSON content, push
events, and the same secret. To run the service at boot without logging in first,
enable lingering once with ``loginctl enable-linger "$USER"``; the VM may require
``sudo`` for that command.

Useful service commands::

    systemctl --user status git-sync
    journalctl --user -u git-sync -f
    systemctl --user restart git-sync
    systemctl --user disable --now git-sync
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import subprocess
import threading
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, request
from waitress import serve


ROOT = Path(__file__).resolve().parent.parent
SOCKET = ROOT / ".git-sync/webhook.sock"
load_dotenv(ROOT / ".env")


def setting(name: str, default: str | None = None) -> str:
    value = os.getenv(name, default)
    if not value:
        raise ValueError(f"{name} must be set in .env")
    return value


PATH = "/" + setting("SYNC_WEBHOOK_PATH", "sync").lstrip("/")
SECRET = setting("SYNC_WEBHOOK_SECRET").encode()
REMOTE = setting("SYNC_REMOTE", "origin")
BRANCH = setting("SYNC_BRANCH", "main")
IMAGE = setting("GEST_IMAGE", "gest-website")

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
log = logging.getLogger("sync_repo")


def run(*command: str, capture: bool = False) -> str:
    log.info("running: %s", " ".join(command))
    result = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE if capture else None,
    )
    return result.stdout.strip() if result.stdout else ""


def sync_repo() -> None:
    branch = run("git", "branch", "--show-current", capture=True)
    if branch != BRANCH:
        raise RuntimeError(f"expected branch {BRANCH!r}, found {branch!r}")
    if run("git", "status", "--porcelain", capture=True):
        raise RuntimeError("working tree is not clean")

    run("git", "pull", "--ff-only", REMOTE, BRANCH)
    commit = run("git", "rev-parse", "--short", "HEAD", capture=True)
    run("docker", "compose", "build")
    run("docker", "image", "tag", f"{IMAGE}:latest", f"{IMAGE}:{commit}")
    log.info("built %s:latest and %s:%s", IMAGE, IMAGE, commit)


class SyncQueue:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.running = False
        self.pending = False

    def trigger(self) -> str:
        with self.lock:
            if self.running:
                self.pending = True
                return "queued"
            self.running = True
        threading.Thread(target=self.work, name="repo-sync", daemon=True).start()
        return "started"

    def work(self) -> None:
        while True:
            try:
                sync_repo()
            except Exception:
                log.exception("sync failed")

            with self.lock:
                if self.pending:
                    self.pending = False
                else:
                    self.running = False
                    return


queue = SyncQueue()


@app.get(PATH)
def health() -> dict[str, str]:
    with queue.lock:
        status = "busy" if queue.running else "ready"
    return {"status": status}


@app.post(PATH)
def webhook() -> tuple[dict[str, str], int] | dict[str, str]:
    signature = request.headers.get("X-Hub-Signature-256", "")
    expected = "sha256=" + hmac.new(SECRET, request.data, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return {"error": "invalid signature"}, 401

    event = request.headers.get("X-GitHub-Event")
    if event == "ping":
        return {"status": "pong"}
    if event != "push":
        return {"status": "ignored"}, 202

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return {"error": "body must be JSON"}, 400
    if payload.get("ref") != f"refs/heads/{BRANCH}":
        return {"status": "ignored"}, 202

    return {"status": queue.trigger()}, 202


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    SOCKET.parent.mkdir(mode=0o755, exist_ok=True)
    if SOCKET.exists():
        if not SOCKET.is_socket():
            raise RuntimeError(f"refusing to replace non-socket path: {SOCKET}")
        SOCKET.unlink()
    serve(
        app,
        unix_socket=str(SOCKET),
        unix_socket_perms="666",
        max_request_body_size=1024 * 1024,
    )


if __name__ == "__main__":
    main()
