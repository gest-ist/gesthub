#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import sys
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from http.cookiejar import CookieJar
from pathlib import Path


UA = "Mozilla/5.0"
WORKERS = 8
DEBUG = False
DEBUG_PREVIEW = 4000

cookies = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))
root_url = ""
sharepoint_token_time = 0.0


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def debug(*args):
    if DEBUG:
        print("[debug]", *args, file=sys.stderr)


def preview(data):
    if data is None:
        return ""
    if not isinstance(data, bytes):
        data = str(data).encode()
    text = data[:DEBUG_PREVIEW].decode(errors="replace")
    if len(data) > DEBUG_PREVIEW:
        text += f"\n... <truncated {len(data) - DEBUG_PREVIEW} bytes>"
    return text


def debug_response(res, body=None):
    debug("response status:", getattr(res, "status", None) or res.getcode())
    debug("response url:", res.geturl())
    debug("response headers:\n" + str(res.headers).rstrip())
    if body is not None:
        debug("response body preview:\n" + preview(body))


def request(url, data=None, headers=None, no_redirect=False):
    headers = {"User-Agent": UA, **(headers or {})}
    if data is not None and not isinstance(data, bytes):
        data = json.dumps(data).encode()
    method = "POST" if data is not None else "GET"
    debug("request:", method, url)
    debug("request headers:", headers)
    if data is not None:
        debug("request body:\n" + preview(data))
    req = urllib.request.Request(url, data=data, headers=headers)
    if no_redirect:
        return urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookies),
            NoRedirect,
        ).open(req)
    return opener.open(req)


def read_json(url, data=None, headers=None):
    with request(url, data=data, headers=headers) as res:
        body = res.read()
        debug_response(res, body)
        try:
            return json.loads(body.decode())
        except json.JSONDecodeError:
            print("JSON decode failed for:", url, file=sys.stderr)
            print(preview(body), file=sys.stderr)
            raise


def share_id(url):
    encoded = base64.urlsafe_b64encode(url.encode()).decode().rstrip("=")
    return f"u!{encoded}"


def api_url(url):
    return f"https://api.onedrive.com/v1.0/shares/{share_id(url)}/root/children"


def clean_name(name):
    return "".join("_" if c in '<>:"\\|?*' else c for c in name).strip() or "_"


def download(url, path):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".part")
    print(f"file {path}")
    with request(url) as res, tmp.open("wb") as out:
        if DEBUG:
            debug_response(res)
        while chunk := res.read(1024 * 1024):
            out.write(chunk)
    tmp.replace(path)


def maybe_refresh_sharepoint_token():
    global sharepoint_token_time
    if time.time() - sharepoint_token_time > 3000:
        try:
            request(root_url).close()
            sharepoint_token_time = time.time()
        except Exception as exc:
            print(f"warning: token refresh failed: {exc}")


def clone_graph_folder(url, out_dir):
    data = read_json(url)
    items = data.get("value", [])

    files = []
    for item in items:
        name = clean_name(item["name"])
        path = out_dir / name
        if "folder" in item:
            clone_graph_folder(item["@odata.id"] + "/children", path)
        elif "file" in item:
            files.append((item.get("@content.downloadUrl") or item["@odata.id"] + "/content", path))

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(lambda args: download(*args), files))

    next_url = data.get("@odata.nextLink")
    if next_url:
        clone_graph_folder(next_url, out_dir)


def get_redirect(url):
    try:
        res = request(url, no_redirect=True)
        if DEBUG:
            debug_response(res)
        res.close()
    except urllib.error.HTTPError as exc:
        debug("response status:", exc.code)
        debug("response url:", exc.url)
        debug("response headers:\n" + str(exc.headers).rstrip())
        if 300 <= exc.code < 400:
            debug("redirect location:", exc.headers["Location"])
            return exc.headers["Location"]
        raise


def sharepoint_listing_url(share_url):
    global sharepoint_token_time

    redirect = get_redirect(share_url)
    if not redirect:
        raise RuntimeError("could not get SharePoint redirect")
    if "Throttle.htm" in redirect:
        raise RuntimeError("SharePoint throttled this request")

    sharepoint_token_time = time.time()
    debug("sharepoint redirect:", redirect)
    debug("cookies:", [cookie.name for cookie in cookies])
    parsed = urllib.parse.urlsplit(redirect)
    qs = urllib.parse.parse_qs(parsed.query)
    folder_id = qs.get("id", [None])[0]
    root_folder = qs.get("RootFolder", [folder_id.rstrip("/") if folder_id else None])[0]
    if not folder_id or not root_folder:
        raise RuntimeError("could not find folder id in SharePoint redirect")

    drive_url = sharepoint_site_url(redirect, folder_id)
    quoted_id = urllib.parse.quote(folder_id, safe="")
    listing_url = (
        drive_url
        + "_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream"
        + f"?@a1=%27{quoted_id}%27&TryNewExperienceSingle=TRUE"
        + "&RootFolder="
        + urllib.parse.quote(root_folder, safe="")
    )
    debug("sharepoint folder id:", folder_id)
    debug("sharepoint root folder:", root_folder)
    debug("sharepoint drive url:", drive_url)
    debug("sharepoint listing url:", listing_url)
    return listing_url


def sharepoint_site_url(redirect, folder_id):
    parsed = urllib.parse.urlsplit(redirect)
    parts = [part for part in folder_id.split("/") if part]
    if len(parts) >= 2 and parts[0] in {"personal", "sites", "teams"}:
        site_path = "/" + "/".join(parts[:2]) + "/"
    else:
        site_path = "/"
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, site_path, "", ""))


def clone_sharepoint_folder(listing_url, out_dir):
    maybe_refresh_sharepoint_token()
    payload = {
        "parameters": {
            "__metadata": {"type": "SP.RenderListDataParameters"},
            "RenderOptions": 464386,
            "AllowMultipleValueFilterForTaxonomyFields": True,
            "AddRequiredFields": True,
        }
    }
    data = read_json(
        listing_url,
        data=payload,
        headers={
            "Accept": "application/json;odata=verbose",
            "Content-Type": "application/json;odata=verbose",
        },
    )

    files = []
    for item in data.get("Row", []):
        api = item.get(".spItemUrl", "").split("?", 1)[0].replace("\\u002f", "/")
        name = clean_name(item.get("FileLeafRef") or item.get("FileRef", "file").rsplit("/", 1)[-1])
        kind = item.get("FSObjType")

        if kind == "1":
            print(f"dir  {out_dir / name}")
            clone_graph_folder(api + "/children", out_dir / name)
        elif kind == "0":
            files.append((api + "/content", out_dir / name))

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(lambda args: download(*args), files))


def main():
    global root_url
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} URL out-dir", file=sys.stderr)
        raise SystemExit(2)

    root_url = sys.argv[1].strip("'\"")
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    if "sharepoint.com" in root_url:
        clone_sharepoint_folder(sharepoint_listing_url(root_url), out_dir)
    else:
        clone_graph_folder(api_url(root_url), out_dir)


if __name__ == "__main__":
    main()
