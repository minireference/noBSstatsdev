# Jupyter Book Styles Sample


## Dev workflow

1. Start the live preview in any styles folder containing `myst.yml`:
   ```bash
   cd sample
   jupyter book start
   ```

2. Click on the printed URL, usually http://localhost:3000.

3. Open the file `sample/theme/custom.css` to edit the custom styles
   for the `sample` styles folder.
   The site should update automatically for each change you make to the .css file.
   Hard-refresh if your browser retains old CSS (CTRL + SHIFT + R).

4. Stop the dev server with `Ctrl+C`. 



## Which style files to edit

| File inside a book folder | Purpose |
| --- | --- |
| `myst.yml` | TOC, title, renderer, logos, and stylesheet registration. |
| `theme/custom.css` | Palette, fonts, spacing, tables, and custom components. |
| `assets/normal-density.png` | An image included in sample content. |
| `assets/*.svg` | Sample logos and favicon. |


- The custom CSS stylesheet is registered in `myst.yml`.
- Colors are defined via `--myst-color-*` variables in `:root` and `.dark`.
- You can edit the content pages to add custom classes
  like `.custom-class-lead` and `.custom-class-card`
  then style them using CSS and  `--custom-class-*` variables.
- Inspect the rendered DOM with browser developer tools to choose element selectors
- Check your styles in all modes:
  - light and dark mode
  - mobile, tablet, and desktop screen widths






## Build static HTML website

To "package" the Jupyter book in the folder `sample`
as a static HTML website, run these command in the repository root:

```bash
python scripts/build.py sample
```

This will run the Jupyter book `build --html` command with:
- working directory set to `sample/`
- the output directory set to `sample/_build/html/`
- the environment variable `BASE_URL=/sample` set
  (which is required for the static site content to be hosted as the subfolder `/sample` on the web server)

More generally, you can use  `python scripts/build.py <folder>`
to build the Jupuyter Book project in the folder `<folder>`.





### Build and preview the static HTML website 

To inspect the results of the static build in `sample/_build/html` run:

```bash
python scripts/build.py sample --serve
```

The script builds the Jupyter book in `sample` then serves
the generated HTML locally at `http://127.0.0.1:8000/sample/`.
To stop the preview sever use `Ctrl+C`.



## Copy a book to start a new version

Copy the complete `sample/` folder to a new direct subfolder.
e.g. copy `sample/` to `styles-v2/` 

The new folder `styles-v2/` will contain independent copies of the configuration,
stylesheet, images, and content. Edit those copies without changing the original `sample/`.
For example, change the color palette in `styles-v2/theme/custom.css`.





## Deployment to web server 

To build and deploy the built HTML from the `sample` Jupyter Book, use:

```bash
python scripts/build.py sample
python scripts/deploy.py sample
```

This recursively uploads the contents of `sample/_build/html/`
to the directory `/var/www/html/sample/`, which gets served
at `https://dev.noBSstats.com/sample/`.

Run the same command again to upload changes. 

Build and deploy the version in `<folder>` by running:

```bash
python scripts/build.py <folder>
python scripts/deploy.py <folder>
```

This may take up to five minutes because there are thousands of files.
View the results at `https://dev.noBSstats.com/<folder>/`.




## Links

- [MyST styles and CSS classes](https://mystmd.org/guide/website-style)
- [Theme colours](https://myst-theme.netlify.app/theming/)
- [Colour picker](https://myst-theme.netlify.app/color-picker/)
- [Jupyter Book 2](https://jupyterbook.org/stable/)
- [Static hosting and BASE_URL](https://mystmd.org/guide/deployment)
