# Homepage sample

This folder contains an starter code for a static homepage for the site.
Use the script `scripts/buildhomepage.py` to build the page
from the page components in the `templates/` directory,
and outputs the built HTML + assets to the `dist/` directory.


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
  dist/                  # build directory
```


- The main file is `templates/index.html` and it includes other HTML fragments
- You can edit each fragment independently.
- Stylesheet is in `homepageassets/styles.css`.



## Build and preview

From the repository root, activate your Python environment and install the
root requirements. If you are adding these files to an older checkout,
install Jinja with `python -m pip install Jinja2` and add it to the root
`requirements.txt`. Add `dist/` to the root `.gitignore` as well.

```bash
python scripts/buildhomepage.py homepage
python -m http.server 8000 --directory homepage/dist
```

Open `http://localhost:8000/`. Stop the preview with Ctrl+C. After editing,
rerun the build in another terminal and refresh the browser.

The value of the variable `site_title` defiend in context dict
in  `buildhomepage.py` supplies `site_title` variable in templates.
Missing template variables are set to produce build errors. 

The output is `homepage/dist/index.html` and `homepage/dist/homepageassets/`.
The builder overwrites matching output files and copies nested assets.



## Dev server with live reload

To run a live-reloading dev server, use the command:

```bash
python ./scripts/buildhomepage.py homepage --serve
```

This will watches the sources and refresh the browser on change.






## Start another version of the homepage

Copy the source folder from the repository root, skipping generated output:

```bash
python -c "import shutil; shutil.copytree('homepage', 'homepage-v2', ignore=shutil.ignore_patterns('dist'))"
python scripts/buildhomepage.py homepage-v2
python ./scripts/buildhomepage.py homepage-v2 --serve
```

Edit its templates and stylesheet independently.




## Deploy to web server

Set the SSH constants at the top of `scripts/deploy.py`, then run:

```bash
python scripts/deploy.py homepage
```

The deployment script will take the contents of `homepage/dist/`
and upload it to `/var/www/html/homepage/`,
which corresponds to the URL: https://dev.noBSstats.com/homepage/ 

Use `scripts/deploy.py` to deploy any other folder.
For example, run `./scripts/deploy.py homepage-v2`
to upload the folder `homepage-v2` to `/var/www/html/homepage-v2/`
which can be viewed online at:  https://dev.nobsstats.com/homepage-v2/ .




## Links


- [Jinja template API](https://jinja.palletsprojects.com/en/stable/api/)
