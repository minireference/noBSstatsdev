#!/usr/bin/env python3
"""Check a specimen build: python scripts/check_build.py <folder>."""

import argparse
import os
import re
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

import nbformat


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


class PageAssets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = []
        self.math_errors = 0

    def handle_starttag(self, tag, attributes):
        attributes = dict(attributes)
        if tag == "img" and attributes.get("src"):
            self.assets.append(attributes["src"])
        if tag == "link" and "stylesheet" in attributes.get("rel", ""):
            self.assets.append(attributes.get("href", ""))
        if "katex-error" in attributes.get("class", "").split():
            self.math_errors += 1


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="Book folder, for example: sample")
    args = parser.parse_args()
    try:
        directory = book_directory(args.folder)
    except ValueError as error:
        parser.exit(1, "Error: " + str(error) + "\n")
    build = os.path.join(directory, "_build", "html")
    failures = []
    pages = ["index.html", "markdownpage/index.html", "notebook/index.html"]
    base_url = "/" + args.folder
    inspected = 0
    for page in pages:
        path = os.path.join(build, page)
        if not os.path.isfile(path):
            failures.append("Missing page: " + page)
            continue
        with open(path, encoding="utf-8") as handle:
            html = handle.read()
        parsed = PageAssets()
        parsed.feed(html)
        if parsed.math_errors:
            failures.append("Math rendering errors in " + page)
        for asset in parsed.assets:
            url = urlsplit(asset)
            if url.scheme or url.netloc or not url.path:
                continue
            asset_path = unquote(url.path)
            if base_url and asset_path.startswith(base_url + "/"):
                asset_path = asset_path[len(base_url):]
            elif asset_path.startswith("/"):
                failures.append("Asset missing " + base_url + " prefix: " + asset)
            if asset_path.startswith("/"):
                local = os.path.join(build, asset_path.lstrip("/"))
            else:
                local = os.path.join(os.path.dirname(path), asset_path)
            if not os.path.isfile(local):
                failures.append("Missing local asset in " + page + ": " + asset)
            inspected += 1

    stylesheet = os.path.join(build, "myst-theme.css")
    if os.path.isfile(stylesheet):
        with open(stylesheet, encoding="utf-8") as handle:
            css = handle.read()
        if "--custom-class-body-font" not in css:
            failures.append("Custom theme CSS was not bundled.")
    else:
        failures.append("Missing custom stylesheet: myst-theme.css")

    notebook = nbformat.read(os.path.join(directory, "content", "notebook.ipynb"), as_version=4)
    nbformat.validate(notebook)
    plots = 0
    for index, cell in enumerate(notebook.cells, start=1):
        if cell.cell_type != "code":
            continue
        if cell.source.strip() and cell.execution_count is None:
            failures.append("Unexecuted notebook cell: " + str(index))
        for output in cell.get("outputs", []):
            if output.output_type == "error":
                failures.append("Notebook error in cell " + str(index))
            if "image/png" in output.get("data", {}):
                plots += 1
    if plots < 2:
        failures.append("Expected at least two saved Seaborn plot outputs.")

    if failures:
        raise SystemExit("\n".join(failures))
    print("PASS: " + args.folder + "; 3 pages, custom CSS, " + str(inspected) + " local asset references,")
    print("      valid executed notebook, " + str(plots) + " plot outputs, no errors.")


if __name__ == "__main__":
    main()

