#!/usr/bin/env python3
"""Tiny static server for local PWA testing (correct MIME types, no HTTP cache)."""
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class Handler(SimpleHTTPRequestHandler):
    extensions_map = {
        **SimpleHTTPRequestHandler.extensions_map,
        ".webmanifest": "application/manifest+json",
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".json": "application/json",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        self.send_header("Service-Worker-Allowed", "/")
        super().end_headers()


if __name__ == "__main__":
    port = 8766
    print(f"http://localhost:{port}/  ({ROOT})")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
