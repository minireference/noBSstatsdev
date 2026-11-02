# noBSstatsdev

Hello World :)

This is the code repo for the Group 882 WE Accelerate internship project,
which is to create a website for the book: **No Bullshit Guide to Statistics**.
The repo contains sample content (`homepage` and `sample`) and scripts (`scripts`)
to facilitate the delivery of the two deliverables for the project:

- D1: new homepage for noBSstats.com   (replacing the current https://noBSstats.com/ )
- D2: styling for content pages like https://nobsstats.com/notebooks/discrete-random-vars/ (book-theme styles customization)



## Sample content

The folders `homepage` and `sample` in the repo serve as the definitions of the "shape"
of the deliverables D1 and D2 I expect by the end of the project.


### Homepage

The folder `homepage/` contains starter code for creating a static
landing page that will live at https://noBSstats.com/ in prod.

The sample code uses the Jinja templates to build `homepage/dist/index.html`
from the template `homepage/templates/index.html`, which in turn includes
the HTML fragments taken from `homepage/templates/`.
The source stylesheet file is `homepage/homepageassets/styles.css`
gets copied to `homepage/dist/homepageassets/styles.css`
along with any other files in the `homepageassets/` folder.


```text
  homepage/
    templates/
      index.html             # main file
      header.html
      footer.html
      ...
    homepageassets/
      styles.css
    README.md
    dist/                    # generated; ignored by Git
```


NOTE: You have complete freedom about the choice of tech stack,
build scripts, and CSS framework you want to use to create the homepage.
The sample code provided in `homepage/` is just one way to do things,
but feel free to ignore everything I have provided, and use another approach.
As long as you have some way to put the required static `index.html` and
js/css/img assets in `homepageassets/` in the directory `<folder>/dist/`,
we good.


The idea is that you will develop different version of the homepage in
separate folders, e.g., `homepage-v2`,  `homepage-v3`, etc., until we get to  `homepage-final`.



### Styles sample

The folder `sample/` contains a sample **Jupyter Book** project with custom styles definitions.

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

Each styles subfolder is independent, with its own `myst.yml` and `theme/custom.css`.
The idea is that you will create multiple copies of this book folder to work on the styles,
e.g. `styles-v1`,  `styles-v2`, `styles-v3`, etc., until we get to  `styles-final`.
The markdown file and notebook in `content/` and images `assets/` can stay the same
across different styles versions, but feel free to modify the files in `content/` as you wish.




## Scripts

The folder `scripts/` contains shared scripts to build `homepage` and `styles` folders.

```text
  scripts/
    buildhomepage.py  # generate <folder>/dist/index.html homepage from <folder>/templates/index.html
    build.py          # generate <folder>/_build/html/index.html  from a book folder
    deploy.py
```

The script `deploy.py` uploads the local `<folder>` to the online server at the URL `https://dev.noBSstats.com/<folder>/`










## 1. Install prerequisites

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








## 2. Create the Python environment

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

Activate the environment again whenever you open a new terminal.







## Dev workflow

We'll use this code repo as a shared workspace for developing several versions
of a the homepage noBSstats.com and the styles for the content pages.
- Use subfolders `<folder>` to store different version of the deliverables
  e.g. `homepage-v2`,  `homepage-v3`, etc., until  `homepage-final`,
  and  `styles-v1`,  `styles-v2`, `styles-v3`, until  `styles-final`.
- Each folder is completely independent, but easily sharable:
  - git add, commit, and push your local folder `homepage-demo` to the main repo 
  - git add, commit, and push local folder `homepage-demo` to a different brach, then open a pull request to the main branch
  - build your local folder `homepage-demo` and upload it to `https://dev.noBSstats.com/<folder>/`, then share this URL



## Build homepage sample  (D1 example)

From the repository root, with the Python environment activated:

```bash
python scripts/buildhomepage.py homepage
python -m http.server 8000 --directory homepage/dist
```

The script builds the homepage in folder `homepage/` then
the second command serves the generated HTML locally at `http://127.0.0.1:8000/`.
Open `http://localhost:8000/` in your browser.
To stop the sever, use `Ctrl+C`.

See `homepage/README.md` for more info.




## Build and run the Jupyter Book Styles Sample  (D2 example)


To view the Jupyter Book sample project with custom styles,
run the command:

```bash
python scripts/build.py sample --serve
```


This script builds the jupyter book in folder `sample/` and outputs
the static site to `sample/_build/html/`,
serves the generated HTML locally at `http://127.0.0.1:8000/sample/`.
Open `http://127.0.0.1:8000/sample/` in your browser.
To stop the sever, use `Ctrl+C`.

See `sample/README.md` for more info.







## Deployment

The script `scripts/deploy.py` allows you to deploy a local HTML build folder
(either from a homepage or a styles deliverable)
to the dev web server at https://dev.noBSstats.com

To deploy the local folder `<folder>`, use the command:

```bash
python scripts/deploy.py <folder>
```

This will upload the HTML build content from the local `<folder>`
so that it gets served online at the public URL `https://dev.noBSstats.com/<folder>/`


The following constants must be set at the top of the script:

```python
SSH_HOST = "dev.noBSstats.com"
SSH_USER = "admin"
SSH_PORT = 22
SSH_PRIVATE_KEY = "credentials/admin_key"  # Private key, not id_rsa.pub.
SSH_KNOWN_HOSTS = "credentials/known_hosts"
```

You may need to edit `SSH_PRIVATE_KEY` if the SSH key is called something else,
e.g. use `SSH_PRIVATE_KEY = "credentials/ivan_key"`
to use the private key `credentials/ivan_key` for SSH authentication to the server.

```text
  credentials/
    admin_key                   # example private key
    admin_key.pub               # matching public key
    known_hosts                 # saved server keys
```


Note: for SSH key authentication to work, the contents of `credentials/ivan_key.pub`
must appear in the file `/home/admin/.ssh/authorized_keys` on the the remote server.
On the first connection to an unknown server, the script will ask you to type `yes`
to the server key to `credentials/known_hosts`. Subsequent runs check the server key
is the same, so you know you're connecting to the same server as on the first connection.
 










## Links

- Production website: https://noBSstats.com/
- Production website source repo: https://github.com/minireference/noBSstats
- Dev wesbite: https://dev.noBSstats.com/
  - See https://dev.noBSstats.com/homepage/ for sample homepage
  - See https://dev.noBSstats.com/sample/ for sample styles
- Dev website source repo: https://github.com/minireference/noBSstatsdev

