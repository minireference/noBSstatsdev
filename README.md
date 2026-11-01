# noBSstatsdev

A small **Jupyter Book 2** workspace for developing several versions of a
book's content and CSS theme side by side. Each book subfolder is an
independent project with its own `myst.yml`, content, assets, theme, and build.
The Python environment and helper scripts are shared at the repository root.

The separate `homepage/` folder is a static landing page built from Jinja
templates and one stylesheet, independently of Jupyter Book.

The included `sample/` book has three pages: an index, a Markdown kitchen
sink, and an executed notebook with text, a DataFrame, two Seaborn plots,
local images, and inline/display mathematics.

## Repository layout

```text
noBSstatsdev/
  README.md
  LICENSE
  .gitignore
  requirements.txt
  requirements-dev.txt
  scripts/
    build.py
    buildhomepage.py
    check_build.py
    deploy.py
  credentials/
    id_rsa                   # your private key; ignored by Git
    id_rsa.pub               # matching public key; ignored by Git
    known_hosts              # saved server identity; ignored by Git
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
    _build/                  # generated; ignored by Git
  homepage/
    templates/
      index.html
      header.html
      footer.html
      ...
    homepageassets/
      styles.css
    README.md
    dist/                    # generated; ignored by Git
```

Place your own keys in `credentials/`. No keys or generated builds are
included in the ZIP.

## 1. Get the files and install prerequisites

After this project has been uploaded to GitHub, clone it with:

```bash
git clone https://github.com/minireference/noBSstatsdev.git
cd noBSstatsdev
```

Alternatively, extract the ZIP and open a terminal in its `noBSstatsdev/`
directory. The commands below assume that directory is the repository root.

Install **Python 3.12**, **Node.js 24 LTS** (including npm), and Git if you
use the clone command. Deployment uses the Python package Paramiko,
included in `requirements.txt`, and a server with SSH/SFTP enabled.
No local `ssh` or `scp` program is needed. No LaTeX installation is
required for the website.

Check the installed versions:

```bash
python --version
node --version
npm --version
```

On macOS/Linux, Python may be named `python3` before you activate the
environment below.

## 2. Create the shared Python environment

Create one environment at the repository root, not one inside each book.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If activation is blocked, call the environment's executables directly,
for example `.\.venv\Scripts\python.exe scripts/build.py sample`.

Confirm the builder version:

```bash
jupyter book --version
```

The requirements pin Jupyter Book **2.1.7**, Paramiko **5.1.0**, Jinja2
**3.1.6**, and the Python packages used by the specimens.
MyST downloads `book-theme` separately: these pins do
not lock every renderer/JavaScript dependency. The first preview or build
needs internet access to obtain the renderer and its dependencies.

Activate the environment again whenever you open a new terminal.

## 3. Develop and preview a book

Start the live preview from the folder containing that book's `myst.yml`:

```bash
cd sample
jupyter book start
```

Open the URL printed by the command, normally `http://localhost:3000`.
Edit `theme/custom.css` and files in `content/` relative to this book's
folder. Save and inspect the updated website. Hard-refresh if your browser
retains old CSS; restart the preview if a file change is not detected.

The live development server normally serves this book at `/`. The static
build script below prepares the published `/sample/` prefix separately.
If you previously set `BASE_URL` in your terminal, unset it before using
the live preview (`unset BASE_URL` in Bash, or
`Remove-Item Env:BASE_URL -ErrorAction SilentlyContinue` in PowerShell).

Stop the preview with Ctrl+C. Return to the repository root with:

```bash
cd ..
```

For another book, run `jupyter book start` inside that other folder.
When previewing two books at once, give them different ports, for example
`jupyter book start --port 3001 --server-port 3101` for the second book.

## 4. Edit the content and CSS

| File inside a book folder | Purpose |
| --- | --- |
| `myst.yml` | TOC, title, renderer, logos, and stylesheet registration. |
| `theme/custom.css` | Palette, fonts, spacing, tables, and custom components. |
| `content/index.md` | A small homepage using the book theme. |
| `content/markdownpage.md` | Headings, prose, lists, tables, images, math, code, admonitions, and tabs. |
| `content/notebook.ipynb` | Executed Python cells, printed output, a DataFrame, and Seaborn figures. |
| `assets/normal-density.png` | Generated image already included in both specimens. |
| `assets/*.svg` | Sample logos and favicon. |

The stylesheet is registered in each book's `myst.yml`:

```yaml
site:
  template: book-theme
  options:
    style: theme/custom.css
```

Paths in this configuration are relative to that book folder. Images in
the Markdown and notebook content use `../assets/normal-density.png`
because the source documents live one level deeper in `content/`.

Start CSS work with the `--myst-color-*` variables in `:root` and `.dark`.
The starter's own classes are `.custom-class-lead` and
`.custom-class-card`; its own CSS variables also use `--custom-class-*`.
Inspect the rendered DOM with browser developer tools before changing
element selectors. Check both specimen pages, light/dark mode, and a
phone-sized viewport. Edit source files rather than generated `_build/`
files. No separate CSS compilation step is needed.

To edit the notebook in JupyterLab, install the optional dependencies
from the repository root:

```bash
python -m pip install -r requirements-dev.txt
jupyter lab
```

Open `sample/content/notebook.ipynb`. After editing Python code, restart
the kernel, run all cells, and save the notebook. The book builder uses
the saved outputs; CSS edits do not require rerunning code. The supplied
notebook already has successful outputs and uses synthetic local data.
Plot colours come from Seaborn/Matplotlib, separately from website CSS.
Standard Markdown images and math work in JupyterLab; MyST-specific
directives are rendered by Jupyter Book.

## 5. Build static HTML for a subfolder URL

From the repository root:

```bash
python scripts/build.py sample
python scripts/check_build.py sample
```

The build script runs `python -m jupyter_book build --html` with:

- working directory: `sample/`;
- `BASE_URL=/sample` in the builder's environment;
- output directory: `sample/_build/html/`.

The environment variable is set inside the script, so the command works
in Bash and PowerShell and does not change your terminal's environment.
Pass one direct folder name, such as `sample` or `design-v2`, using
letters, digits, hyphens, or underscores. Names must start with a letter
or digit. Helper scripts resolve this name relative to the repository,
so they also work when invoked from another working directory.

The sample's published routes are `/sample/`, `/sample/markdownpage/`,
and `/sample/notebook/`. The checker verifies these three specimen pages,
stylesheet/image paths and their URL prefixes, math rendering, and saved
notebook outputs. Adjust the checker if you change the specimen structure.

To inspect the exact static build locally at its published URL prefix:

```bash
python scripts/build.py sample --serve
```

Open `http://127.0.0.1:8000/sample/`. The script builds first, then mounts
the generated HTML at `/sample/`; stop it with Ctrl+C. Use `--port 8001`
if port 8000 is busy. This static preview does not watch source changes:
stop and rerun after edits, or use the live preview while developing.
Opening the generated `index.html` directly, or serving it at `/` without
the prefix, will not resolve the `/sample/...` asset URLs correctly.

## 6. Copy a book to start a new design version

From the repository root, copy the complete `sample/` folder to a new
direct subfolder. This Python command works on macOS, Linux, and Windows
and skips generated `_build/` files and notebook checkpoints:

```bash
python -c "import shutil; shutil.copytree('sample', 'design-v2', ignore=shutil.ignore_patterns('_build', '.ipynb_checkpoints'))"
```

`design-v2/` must not already exist. The new folder contains independent
copies of the configuration, stylesheet, images, and content. Edit those
copies without changing the original `sample/`. For example, change the
project title and `site.options.logo_text` in `design-v2/myst.yml` and
the palette in `design-v2/theme/custom.css`.

Preview that version:

```bash
cd design-v2
jupyter book start
```

Stop the preview, return to the repository root, then build and inspect:

```bash
cd ..
python scripts/build.py design-v2
python scripts/check_build.py design-v2
python scripts/build.py design-v2 --serve
```

Open `http://127.0.0.1:8000/design-v2/` for the static preview. Its output
lives in `design-v2/_build/html/` and its published prefix is
`/design-v2/`. The scripts derive both from the folder name: do not
hard-code a version's `BASE_URL` in `myst.yml`. No new environment or
script edits are needed for each version.

## 7. Build the Jinja homepage

From the repository root, with the Python environment activated:

```bash
python -m pip install -r requirements.txt
python scripts/buildhomepage.py homepage
python -m http.server 8000 --directory homepage/dist
```

Open `http://localhost:8000/`. Edit the fragments in `homepage/templates/`
and the single stylesheet `homepage/homepageassets/styles.css`. Rebuild after edits
and refresh the browser. The script combines `index.html`, `header.html`,
`herosection.html`, `books.html`, and `footer.html`, then copies the assets.
Output lives in `homepage/dist/`. Missing template variables are errors.

All asset URLs are relative, so the same output works at `/` or
`/homepage/`. This build needs Python and Jinja; it has no Jupyter Book or
Node.js build step. See `homepage/README.md` for details and the command to
copy this folder to `homepage-v2/` for another design iteration.

## 8. Configure Python deployment

Open `scripts/deploy.py` and set the constants at the top once for this
project:

```python
SSH_HOST = "your-server.example.com"
SSH_USER = "your-ssh-user"
SSH_PORT = 22
SSH_PRIVATE_KEY = "credentials/id_rsa"
SSH_KNOWN_HOSTS = "credentials/known_hosts"
WEBROOT = "/var/www/html"
```

`SSH_HOST` is a hostname or IP address, without `https://` or a path.
`WEBROOT` is the absolute directory served by your web server. The SSH
user needs write access to it. Key file paths are relative to the
repository root, regardless of the terminal's current directory.

Place your existing **private key** at `credentials/id_rsa`, or change
`SSH_PRIVATE_KEY` to its actual path. An Ed25519 key such as
`credentials/id_ed25519` also works. The matching public key (`.pub`)
must be installed in the server account's `~/.ssh/authorized_keys`.
A public key alone cannot authenticate the connection.

If needed, create the local credentials directory from the repository root:

```bash
python -c "import os; os.makedirs('credentials', exist_ok=True)"
```

The script prompts for a passphrase if the private key is encrypted.
On the first connection to an unknown server, it displays the server's
SHA256 host-key fingerprint. Verify it against your server's fingerprint,
then type `yes` to save it in `credentials/known_hosts`. Subsequent runs
check the saved key. Existing keys in `~/.ssh/known_hosts` are also used.
The entire `credentials/` folder is ignored by Git.

All authentication and uploads use Paramiko's Python APIs. The script
uses no system SSH/SCP programs and executes no remote shell commands.
There is no deployment JSON file or connection-settings command line.

## 9. Deploy a design version

`deploy.py <folder>` selects `<folder>/dist/` if that directory exists;
otherwise it selects `<folder>/_build/html/`. The selected directory must
contain `index.html`. An existing empty `dist/` produces an error.

For the Jinja homepage:

```bash
python scripts/buildhomepage.py homepage
python scripts/deploy.py homepage
```

This uploads `homepage/dist/` into `WEBROOT/homepage/`.

For a Jupyter Book, build and deploy the same folder name from the repository
root:

```bash
python scripts/build.py sample
python scripts/check_build.py sample
python scripts/deploy.py sample
```

This recursively uploads `sample/_build/html/` directly into
`/var/www/html/sample/`, including nested folders and dotfiles. Your web
server can then serve it at `https://YOUR-DOMAIN/sample/`.

Run the same command again to upload changes. Matching remote files are
overwritten; other remote files are left in place. There is no overwrite
flag, staging directory, backup, or deletion step.

Deploy another version with:

```bash
python scripts/build.py design-v2
python scripts/deploy.py design-v2
```

Its destination is `/var/www/html/design-v2/`. The folder name is the only
deployment argument. Every script is self-contained.

On macOS/Linux you can also run `./scripts/build.py sample` and
`./scripts/deploy.py sample`. The `python` form works on Windows as well.

## Documentation

- [Jupyter Book 2](https://jupyterbook.org/stable/)
- [MyST styles and CSS classes](https://mystmd.org/guide/website-style)
- [Theme colours](https://myst-theme.netlify.app/theming/)
- [Colour picker](https://myst-theme.netlify.app/color-picker/)
- [Static hosting and BASE_URL](https://mystmd.org/guide/deployment)
- [Jinja template API](https://jinja.palletsprojects.com/en/stable/api/)
- [Paramiko Python SSH client](https://docs.paramiko.org/en/stable/api/client.html)
- [Paramiko SFTP API](https://docs.paramiko.org/en/stable/api/sftp.html)
