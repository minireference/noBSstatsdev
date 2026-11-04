# Homepage sample

This folder contains starter code for a static homepage for the site.
Use the script `scripts/buildhomepage.py` to build the page
from the page components in the `templates/` directory,
and output the built HTML + assets to the `dist/` directory.


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


- The main file is `templates/index.html`;
  it includes other HTML fragments from the `templates/` folder.
- You can edit each fragment independently.
- Stylesheet is in `homepageassets/styles.css`.



## Build and preview

From the repository root, run:

```bash
python scripts/buildhomepage.py homepage
python -m http.server 8000 --directory homepage/dist
```

Open `http://localhost:8000/`. Stop the preview with Ctrl+C. After editing,
rerun the build in another terminal and refresh the browser.

The value of the variable `site_title` defined in context dict
in  `buildhomepage.py` supplies `site_title` variable in templates.
Missing template variables are set to produce build errors. 

The output is `homepage/dist/index.html` and `homepage/dist/homepageassets/`.
The builder overwrites matching output files and copies nested assets.



## Local dev server with live reload

To run a live-reloading dev server, use the command:

```bash
python ./scripts/buildhomepage.py homepage --serve
```

This watches the sources and refreshes the browser on change.









## Deploy to web server

Set the SSH constants at the top of `scripts/deploy.py`, then run:

```bash
python scripts/deploy.py homepage
```

The deployment script will take the contents of `homepage/dist/`
and upload it to `/var/www/html/homepage/`,
which corresponds to the URL: https://dev.noBSstats.com/homepage/ 




## Start another version of the homepage


- Copy the folder `homepage` to a new folder, e.g. `homepage-v2`.
- Edit the HTML template and stylesheets in the `homepage-v2/`
- Run this command to build and serve the contents of the new folder:
  ```cmd
  python ./scripts/buildhomepage.py homepage-v2 --serve
  ```

When you want to share the preview of the new page,
run `python scripts/deploy.py homepage-v2`
to upload the folder `homepage-v2` to `/var/www/html/homepage-v2/`
which can be viewed online at:  https://dev.nobsstats.com/homepage-v2/




## Links


- [Jinja template API](https://jinja.palletsprojects.com/en/stable/api/)
