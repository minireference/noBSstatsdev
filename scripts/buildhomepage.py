#!/usr/bin/env python3
"""
Build the homepage design: <folder>/templates/ + <folder>/homepageassets/  -->  <folder>/dist/
- Run `./scripts/buildhomepage.py <folder>` to build homepage design in <folder>.
- Run `./scripts/buildhomepage.py <folder> --serve` to run a livereload dev server
  that watches the sources and refresh the browser on change.
"""

import argparse
import os
import re
import shutil
import sys

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    TemplateError,
    select_autoescape,
)


SITE_TITLE = "Minireference"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def build_homepage(directory):
    """Render the page and copy homepageassets into dist."""
    templates = os.path.join(directory, "templates")
    homepageassets = os.path.join(directory, "homepageassets")
    dist = os.path.join(directory, "dist")

    env = Environment(
        loader=FileSystemLoader(templates),
        autoescape=select_autoescape(["html"]),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )

    # These are variables you pass in when building the homepage
    context = {
        "site_title": "No Bullshit Guide to Statistics"
    }
    # IDEAS:
    #   - you could add the text of user reviews here
    #     to avoid having to copy-paste the text manually
    #     in the `<folder>/templates/bookreviews.html` source.

    html = env.get_template("index.html").render(context)

    os.makedirs(dist, exist_ok=True)
    output = os.path.join(dist, "index.html")
    with open(output, "w", encoding="utf-8") as handle:
        handle.write(html)
    if os.path.isdir(homepageassets):
        shutil.copytree(
            homepageassets, os.path.join(dist, "homepageassets"),
            dirs_exist_ok=True,
        )
    print("Built:", output, flush=True)


def serve_homepage(directory, port):
    """
    Serve the contents of `<folder>/dist/`,
    then watch source directories templates/ and homepageassets/ for changes.
    Tell the browser to refresh on change to make webdev/webdesign loop go faster.
    """
    # A one-off build does not need the development server dependency.
    from livereload import Server
    from livereload.handlers import LiveReloadHandler
    from livereload.watcher import Watcher

    def rebuild():
        try:
            build_homepage(directory)
        except (OSError, TemplateError) as error:
            # Keep watching so the next edit can fix the error.
            print("Build failed:", error, file=sys.stderr, flush=True)

    # In livereload 2.7.1, the default three-second throttle drops rapid saves.
    LiveReloadHandler.DEFAULT_RELOAD_TIME = 0
    server = Server(watcher=Watcher())
    server.setHeader("Cache-Control", "no-store")
    server.watch(os.path.join(directory, "templates"), rebuild)
    server.watch(os.path.join(directory, "homepageassets"), rebuild)
    print("Preview: http://127.0.0.1:" + str(port) + "/", flush=True)
    print("Watching templates/ and homepageassets/. Stop with Ctrl+C.", flush=True)
    server.serve(
        root=os.path.join(directory, "dist"),
        host="127.0.0.1",
        port=port,
        live_css=False,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="Homepage folder, for example: homepage")
    parser.add_argument(
        "--serve", action="store_true",
        help="Build, serve, and refresh the browser after source changes.",
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Preview server port (default: 8000).",
    )
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", args.folder):
        parser.error("Use a single folder name such as homepage or homepage-v2.")
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535.")

    directory = os.path.join(ROOT, args.folder)
    try:
        build_homepage(directory)
        if args.serve:
            serve_homepage(directory, args.port)
    except ImportError:
        parser.exit(
            1, "Live preview requires livereload. Install it with:\n"
            "python -m pip install livereload==2.7.1\n",
        )
    except (OSError, TemplateError) as error:
        parser.exit(1, "Error: " + str(error) + "\n")
    except KeyboardInterrupt:
        print("\nPreview stopped.")


if __name__ == "__main__":
    main()
