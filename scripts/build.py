#!/usr/bin/env python3
"""Build a book for /<folder>/; optionally preview that exact static build."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os
import re
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def book_directory(name):
    """Resolve a book folder relative to this repository."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", name):
        raise ValueError("Use a single folder name such as sample or design-v2.")
    directory = os.path.join(ROOT, name)
    if os.path.islink(directory):
        raise ValueError("The book folder must be a directory, not a symlink.")
    if not os.path.isfile(os.path.join(directory, "myst.yml")):
        raise ValueError("No myst.yml found in " + directory)
    return directory


def serve(directory, name, port):
    """Mount generated HTML at its BASE_URL without copying the build files."""
    base_url = "/" + name

    class Handler(SimpleHTTPRequestHandler):
        def route(self):
            path = urlsplit(self.path).path
            if path == base_url:
                self.send_response(302)
                self.send_header("Location", base_url + "/")
                self.end_headers()
                return False
            if not path.startswith(base_url + "/"):
                self.send_error(404, "Open " + base_url + "/")
                return False
            return True

        def do_GET(self):
            if self.route():
                super().do_GET()

        def do_HEAD(self):
            if self.route():
                super().do_HEAD()

        def translate_path(self, path):
            # Leave self.path intact so directory redirects keep /<folder>/.
            return super().translate_path(path[len(base_url):])

    handler = partial(Handler, directory=directory)
    with ThreadingHTTPServer(("127.0.0.1", port), handler) as server:
        print(
            "Serving http://127.0.0.1:" + str(port) + base_url + "/ "
            "(Ctrl+C to stop)", flush=True,
        )
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nPreview stopped.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="Book folder, for example: sample")
    parser.add_argument(
        "--serve", action="store_true",
        help="After building, serve the HTML at /<folder>/ on localhost.",
    )
    parser.add_argument("--port", type=int, default=8000, help="Preview port (8000).")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")

    try:
        directory = book_directory(args.folder)
        environment = os.environ.copy()
        environment["BASE_URL"] = "/" + args.folder
        command = [sys.executable, "-m", "jupyter_book", "build", "--html"]
        print("Building " + args.folder + " with BASE_URL=" + environment["BASE_URL"], flush=True)
        subprocess.run(command, cwd=directory, env=environment, check=True)
        output = os.path.join(directory, "_build", "html")
        if not os.path.isfile(os.path.join(output, "index.html")):
            raise ValueError("Build did not produce " + os.path.join(output, "index.html"))
        print("HTML: " + output, flush=True)
        if args.serve:
            serve(output, args.folder, args.port)
    except (ValueError, OSError) as error:
        parser.exit(1, "Error: " + str(error) + "\n")
    except subprocess.CalledProcessError as error:
        parser.exit(error.returncode or 1, "Jupyter Book build failed.\n")


if __name__ == "__main__":
    main()
