# Jupyter Book Styles Sample


This folder contains a sample **Jupyter Book 2** project with custom styles definitions.


```text
  sample/
    myst.yml
    assets/
    theme/
      custom.css
      README.md
    content/
      index.md
      markdownpage.md
      notebook.ipynb
    _build/
```




### Dev workflow for deliverable 2

To work on the Jupyter Book 2 in the `sample/` folder,
you need to:


1. Open a new command prompt
   and navigate to the project root folder using `cd` commands.
   For example,
   if you cloned the repo to the folder `C:\Users\<your_name>\Projects\c`
   you need to use the following commands
   ```cmd
   cd Projects
   cd noBSstatsdev
   ```

2. Activate the Python virtual environment:
   ```cmd
   .venv\Scripts\activate.bat
   python -m pip install -r requirements-styles.txt
   ```
   You only need to install the requirements the first time.

3. Navigate to the folder containing the version you want to work on
   ```cmd
   cd sample
   ```   

4. Start the Jupyter Book dev server
   ```cmd
    jupyter book start
    ```
    This will run the Jupyter Book project in the `sample` folder
    and serve the generated HTML locally at `http://localhost:3000`.
    To stop the preview server use `Ctrl+C`.

5. Open the file `theme/custom.css` to edit the custom styles
   for the `sample` styles folder.
   The site should update automatically for each change you make to the .css file.
   Hard-refresh if your browser retains old CSS (CTRL + SHIFT + R).





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
as a static HTML website, run this command in the repository root:

```bash
python scripts/buildstyles.py sample
```

This will run the Jupyter book `build --html` command with:
- working directory set to `sample/`
- the output directory set to `sample/_build/html/`
- the environment variable `BASE_URL=/sample` set
  (which is required for the static site content to be hosted as the subfolder `/sample` on the web server)

More generally, you can use  `python scripts/buildstyles.py <folder>`
to build the Jupyter Book project in the folder `<folder>`.






## Deployment to web server 

To build and deploy the built HTML from the `sample` Jupyter Book, use:

```bash
python scripts/buildstyles.py sample
python scripts/deploy.py sample
```

This recursively uploads the contents of `sample/_build/html/`
to the directory `/var/www/html/sample/`, which gets served
at `https://dev.noBSstats.com/sample/`.

Run the same command again to upload changes. 




## Copy the sample folder to start a new version

Copy the complete `sample/` folder to a new direct subfolder.
e.g. copy `sample/` to `styles-v2/` and work on the copy.

- The new folder `styles-v2/` will contain independent copies of the configuration,
  stylesheet, images, and content. Edit those copies without changing the original `sample/`.
  For example, change the colour palette in `styles-v2/theme/custom.css`.
- The idea is that you will create multiple copies of this book folder to work on the styles,
  e.g. `styles-v1`,  `styles-v2`, `styles-v3`, etc., until we get to  `styles-final`.
- The markdown file and notebook in `content/` and images in `assets/` can stay the same
  across different styles versions, but feel free to modify the files in `content/` as you wish.

Build and deploy the version in `styles-v2` by running:

```bash
python scripts/buildstyles.py styles-v2
python scripts/deploy.py styles-v2
```

This may take up to five minutes because there are thousands of files.
View the results at `https://dev.noBSstats.com/styles-v2/`.




## Links

- [MyST styles and CSS classes](https://mystmd.org/guide/website-style)
- [Theme colours](https://myst-theme.netlify.app/theming/)
- [Colour picker](https://myst-theme.netlify.app/color-picker/)
- [Jupyter Book 2](https://jupyterbook.org/stable/)
- [Static hosting and BASE_URL](https://mystmd.org/guide/deployment)
