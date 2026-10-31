# Jinja homepage

This folder is an independent static landing page. The shared
`scripts/buildhomepage.py` script renders the templates and copies assets.

```text
homepage/
  templates/
    index.html
    header.html
    hersection.html
    books.html
    footer.html
  homepageassets/
    styles.css
  dist/                  # generated; ignored by Git
```

`templates/index.html` includes the four HTML fragments. Edit each fragment
independently. All styles are in `homepageassets/styles.css`. The `hersection.html`
filename matches the supplied folder plan.

## Build and preview

From the repository root, activate your Python environment and install the
root requirements. If you are adding these files to an older checkout,
install Jinja with `python -m pip install Jinja2` and add it to the root
`requirements.txt`. Add `dist/` to the root `.gitignore` as well.

```bash
python -m pip install -r requirements.txt
python scripts/buildhomepage.py homepage
python -m http.server 8000 --directory homepage/dist
```

Open `http://localhost:8000/`. Stop the preview with Ctrl+C. After editing,
rerun the build in another terminal and refresh the browser.

`SITE_TITLE` at the top of `buildhomepage.py` supplies `site_title` to the
templates. Missing template variables produce a build error. HTML-sensitive
characters in template variables are escaped automatically.

The output is `homepage/dist/index.html` and `homepage/dist/assets/`.
The builder overwrites matching output files and copies nested assets.
Remove `dist/` before rebuilding if you want to discard obsolete output
files. The build script does not modify the source templates or assets.

Relative asset links work when the site is served either at `/` or under
`/homepage/`. No `BASE_URL`, Node.js, or Jupyter Book step is needed for
this homepage build. Jinja and Python are needed only during the build.

## Start another version

Copy the source folder from the repository root, skipping generated output:

```bash
python -c "import shutil; shutil.copytree('homepage', 'homepage-v2', ignore=shutil.ignore_patterns('dist'))"
python scripts/buildhomepage.py homepage-v2
python -m http.server 8000 --directory homepage-v2/dist
```

The new directory must not already exist. Edit its templates and stylesheet
independently. Stop another preview on port 8000 before starting this one,
or choose a different port.

## Deploy

Set the SSH constants at the top of `scripts/deploy.py`, then run:

```bash
python scripts/deploy.py homepage
```

The deployment script prefers `homepage/dist/` when that directory exists.
Otherwise it selects `homepage/_build/html/`. The selected output must have
an `index.html`; an empty `dist/` produces an error.

With the default `WEBROOT`, output is uploaded into
`/var/www/html/homepage/`. Only the generated files are deployed. The web
server needs no Python or Jinja installation. The same command with
`homepage-v2` uploads that version into `/var/www/html/homepage-v2/`.
