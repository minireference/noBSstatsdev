#!/usr/bin/env python3
"""Render <folder>/templates/index.html and copy homepageassets into <folder>/dist/."""

import argparse
import os
import re
import shutil

from jinja2 import (
    Environment,
    FileSystemLoader,
    StrictUndefined,
    TemplateError,
    select_autoescape,
)


SITE_TITLE = "Minireference"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="Homepage folder, for example: homepage")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", args.folder):
        parser.error("Use a single folder name such as homepage or homepage-v2.")

    directory = os.path.join(ROOT, args.folder)
    templates = os.path.join(directory, "templates")
    homepageassets = os.path.join(directory, "homepageassets")
    dist = os.path.join(directory, "dist")

    try:
        env = Environment(
            loader=FileSystemLoader(templates),
            autoescape=select_autoescape(["html"]),
            undefined=StrictUndefined,
            keep_trailing_newline=True,
        )
        html = env.get_template("index.html").render(site_title=SITE_TITLE)

        os.makedirs(dist, exist_ok=True)
        output = os.path.join(dist, "index.html")
        with open(output, "w", encoding="utf-8") as handle:
            handle.write(html)
        if os.path.isdir(homepageassets):
            shutil.copytree(
                homepageassets, os.path.join(dist, "homepageassets"), dirs_exist_ok=True,
            )
        print("Built:", output)
    except (OSError, TemplateError) as error:
        parser.exit(1, "Error: " + str(error) + "\n")


if __name__ == "__main__":
    main()
