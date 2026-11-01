# Homepage

This folder contains an started code for a static homeapge for the site.
Use the script `scripts/buildhomepage.py` to build the page
from the page components in the `templates/` directory,
and outputs the build HTML + assets to the `dist/` directory.


```text
homepage/
  templates/
    index.html           # main file
    header.html
    herosection.html
    books.html
    footer.html
  homepageassets/
    styles.css
  dist/                  # build directory; ignored by Git
```

THe 
- The main file is `templates/index.html` and it includes other HTML fragments
- You can edit each fragment independently.
- Style styles are in `homepageassets/styles.css`.


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
Jinja and Python are needed during the build.


## Start another version of the homepage

Copy the source folder from the repository root, skipping generated output:

```bash
python -c "import shutil; shutil.copytree('homepage', 'homepage-v2', ignore=shutil.ignore_patterns('dist'))"
python scripts/buildhomepage.py homepage-v2
python -m http.server 8000 --directory homepage-v2/dist
```

Edit its templates and stylesheet independently.
Stop another preview on port 8000 before starting this one,
or choose a different port.


## Deploy to web server

Set the SSH constants at the top of `scripts/deploy.py`, then run:

```bash
python scripts/deploy.py homepage
```

The deployment script will take the contents of `homepage/dist/`
and upload it to `/var/www/html/homepage/`,
which corresponds to the URL: https://dev.nobsstats.com/homepage/ 
The same command with `homepage-v2` uploads that version to `/var/www/html/homepage-v2/`
which can be viweed online at:  https://dev.nobsstats.com/homepage-v2/ .
