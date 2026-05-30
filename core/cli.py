"""Command-line entry points for local project administration."""

from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Sequence


def manage() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)


def run_commands(commands: Sequence[Sequence[str]]) -> int:
    for command in commands:
        completed = subprocess.run(command, check=False)
        if completed.returncode != 0:
            return completed.returncode
    return 0


def check() -> int:
    return run_commands(
        (
            ("manage", "check"),
            ("ruff", "check", "."),
            ("ruff", "format", "--check", "."),
            ("ty", "check"),
        )
    )


def fix() -> int:
    return run_commands(
        (
            ("ruff", "check", "--fix", "."),
            ("ruff", "format", "."),
        )
    )
