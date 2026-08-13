#!/usr/bin/env python3
"""Local preview server that never lets the browser cache assets.

Plain `python3 -m http.server` allows heuristic caching, so edits to CSS/JS
appear to have no effect until a hard refresh. Use this while developing.
"""
import functools, http.server, socketserver, sys


class Threaded(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True

class NoCache(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, max-age=0")
        super().end_headers()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 4173
    with Threaded(("", port), functools.partial(NoCache, directory=".")) as httpd:
        print(f"serving on {port}")
        httpd.serve_forever()
