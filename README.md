# noBSstatsdev

Hello World :)

This is the code repo for the Group 882 WE Accelerate internship project,
which is to create a website for the book: **No Bullshit Guide to Statistics**.
The repo contains sample content (`homepage` and `sample`) and scripts (`scripts`)
to facilitate the delivery of the two deliverables for the project:

- D1: new homepage for noBSstats.com   (replacing the current https://noBSstats.com/ )
- D2: styling for content pages like https://nobsstats.com/notebooks/discrete-random-vars/ (book-theme styles customization)



## 0. Setting up your local dev environment (Windows)


### Step 0.0: Open a command line prompt

- Click the start menu and start typing `cmd` on the keyboard.
- Run `Command Prompt` to open the command line interface:
  this is a text interface for running programs on your computer.
  You type in short input text commands here and press ENTER to run them,
  then output of the command is displayed below as text.
  For example, type in the command `dir`
  to see the contents of your home directory.
- We'll learn about other commands below.
  I know this looks complicated, but don't worry, you can do this!



### Step 0.1: Install SSH client

SSH allows you to connect and control remote servers.
You can enable SSH from Windows Settings using the following steps:

1. Open **Settings** (Press `Win + I`).
2. Navigate to **Apps** \> **Optional features** (On Windows 11, it may be under **System** \> **Optional features**).
3. Look through the list of **Installed features**. If **OpenSSH Client** is already there, you are good to go.
4. If it isn't listed, click **View features** (or **Add a feature**).
5. Type **OpenSSH Client** into the search bar, check its box, and click **Install**.


### Step 0.2: Install a Git client

- Option 1: use GitHub Desktop GUI app.  
  Download and install from https://github.com/apps/desktop
- Option 2: use git on the command line.  
  Download and install from https://git-scm.com/install/windows

We'll install both so you can start using GitHub Desktop GUI for the first two weeks,
then, optionally, learn to use the `git` on the command prompt later on.


### Step 0.3: Download and install Python

- Download Python 3.14 from
  https://www.python.org/downloads/release/python-31410/


### Step 0.4: Download and install Node.js

- Download from https://nodejs.org/en/download
  Use the installer from the bottom of the page below "Or get a prebuilt Node.js for Windows..."	


### Checks

At this point you should have SSH, Git, Python, and Node.js installed on your machine.
You can check the above installation steps worked by opening a new command prompt
and typing the following commands (one line at a time),
which will print the installed versions:

```cmd
ssh -V
git --version
python --version
node --version
```

We don't need any specific version to proceed.
We're just checking the programs `ssh`, `git`, `python`, `node`
are all available to run on the command line.





## 1. Clone repo and check prerequisites

The next step is to **clone** the `noBSstatsdev` code repository
which lives at https://github.com/minireference/noBSstatsdev on GitHub.
Cloning is fancy tech jargon for making a local copy of the remote repository,
while keeping a link to where the code came from so you can push changes back upstream.

- Option 1: use GitHub Desktop GUI app to clone the repo to your computer.
  Choose a local location that doesn't have forward slashes or spaces.
  - Recommended: directly in your home folder `C:\Users\<your_name>`
    or a subfolder `C:\Users\<your_name>\Projects`.
  
- Option 2: use git on the command line to clone the repo.
  - Open a new command prompt
  - Optionally use `cd` navigate to the directory when you want to work in.
    For example, `cd Projects` to go inside the `C:\Users\<your_name>\Projects` folder.
  - Run the git clone command as follows:
    ```cmd
    git clone https://github.com/minireference/noBSstatsdev.git
    ```

### Checks

At this point you should have the folder `noBSstatsdev` on your computer.
Use the command line prompts to go inside the project folder and list its contents:

```cmd
cd noBSstatsdev
dir
```

Open the graphical user interface (File Explorer) to view the contents as well.
Use our favourite text editor (e.g. VS Code) to look around the `noBSstatsdev` folder.

All the commands in this README assume that you are running them in a command line
terminal inside the `noBSstatsdev` directory (the repository root).






## 2. Install Python libraries in a virtual environment


The next step is to create a Python "virtual environment" for the project,
where we'll install all the libraries and tools we use for the project.

Use the command line to navigate to the `noBSstatsdev` directory then run:


### Windows command prompt

Run these commands line-by-line on the command prompt:

```cmd
python -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

You'll need to run the command `.venv\Scripts\activate.bat` every time you open a new commend line 
to activate the environment again whenever you open a new terminal.


### macOS / Linux

Run these commands line-by-line in a terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

You'll need to run the command `source .venv/bin/activate` whenever you open a new terminal
to activate the environment.








## Sample content

The folders `homepage` and `sample` in the repo define the "shape"
of the deliverables D1 and D2 I expect by the end of the project.


### Homepage starter code

The folder `homepage/` contains starter code for creating a static
landing page that will live at https://noBSstats.com/ in prod.

The sample code uses the Jinja templates to build `homepage/dist/index.html`
from the template `homepage/templates/index.html`, which includes
HTML fragments taken from the `homepage/templates/` directory.
The source stylesheet file `homepage/homepageassets/styles.css`
gets copied to `homepage/dist/homepageassets/styles.css`
along with any other files in the `homepageassets/` folder.


```text
  homepage/
    templates/
      index.html             # main file that includes other files
      header.html            # homepage header section
      footer.html            # homepage footer section
      ...
    homepageassets/          # folder for stylesheets, js scripts, and images
      styles.css             # stylesheet used by index.html
    README.md
    dist/                    # build outputs that get uploaded to the server
```


NOTE: You have complete freedom about the choice of tech stack,
build scripts, and CSS framework you want to use to create the homepage.
The sample code provided in `homepage/` is just one way to do things,
but feel free to ignore everything I have provided, and use another approach.
As long as you have some way to put the required static `index.html` and
js/css/img assets in `homepageassets/` in the directory `<folder>/dist/`,
we good.


The idea is that you will develop different versions of the homepage in
separate folders, e.g., `homepage-v2`,  `homepage-v3`, etc., until we get to  `homepage-final`.


### Scripts

The folder `scripts/` contains scripts to help you work with code in the `homepage/`
and other folders `homepage-v2`,  `homepage-v3`, etc.

- Running the script `scripts/buildhomepage.py <folder>`
  will generate `<folder>/dist/index.html` from `<folder>/templates/index.html`.
  See section **Build homepage sample** below for the details.

- You can then use the script `scripts/deploy.py <folder>` to upload the local contents
  of `<folder>/dist/` to the online server,
  so that you can view it at the URL `https://dev.noBSstats.com/<folder>/`.
  See section **Deploy a local folder to the web server** below for the details.



### Styles sample

The folder `sample/` contains a sample **Jupyter Book 2** project with custom styles definitions.
This is your starter code for Deliverable 2, which we'll discuss starting Week 3 of the project.

The relevant info is in [`sample/README.md`](./sample/README.md).








## Build homepage sample

The source files `homepage/templates/` cannot be viewed directly in the browser
since they are separate fragments and need to be "assembled" to form the complete web page.
This process is called a "build" and performed by the script `scripts/buildhomepage.py`.
 
Each time you want to work on the `homepage`, follow these steps:

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
   ```

3. Run the command to build the webpage and start the dev server:
   ```cmd
   python scripts/buildhomepage.py homepage --serve
   ```
   This command serves the generated HTML locally at `http://127.0.0.1:8000/`.
   Click on the link displayed: `http://127.0.0.1:8000/`.
   To stop the dev server, use `Ctrl+C` in the command prompt.


See [`homepage/README.md`](./homepage/README.md) for more info.





## Deployment

The webpage in `homepage/dist/index.html` lives only on your machine,
so there is no way for others to see it.
If we copy the contents of `homepage/dist/`
to the web server `dev.noBSstats.com`,
we can make the page publicly viewable at `https://dev.noBSstats.com/homepage/`.
Copying the local folder to a remote server is called "deploying" in web dev jargon.

The script `scripts/deploy.py` automates this upload process,
as described below, but first we need to do some crypto....



### Generate SSH keypair

In order to connect to the server,
you need to create SSH keys that you'll use to authenticate to the server.

1. Open a new command prompt
   and navigate to the `credentials` directory inside the project root folder
   using `cd` commands.
   For example,
   if you cloned the repo to the folder `C:\Users\<your_name>\Projects\noBSstatsdev`
   you need to use the following commands:
   ```cmd
   cd Projects
   cd noBSstatsdev
   cd credentials
   ```

2. Generate an SSH key pair using the commands
   ```cmd
   ssh-keygen -f admin_key
   ```
   This command will create two files:
   the private key `credentials/admin_key`,
   and the public key `credentials/admin_key.pub`.

3. Send the public key to Ivan so he can add it to
   the file `/home/admin/.ssh/authorized_keys` on the remote server.
   The idea behind SSH key authentication
   is that the server lets in anyone who possesses a private key
   matching one of the authorized public keys.




#### Deploy a local folder to the web server

The script `scripts/deploy.py` deploys a local HTML build folder
(either from a homepage or a styles deliverable)
to the dev web server at https://dev.noBSstats.com

To build and deploy contents of the `homepage` folder:

1. Open a new command prompt 
   and navigate to the project root folder using `cd` commands.
   For example,
   if you cloned the repo to the folder `C:\Users\<your_name>\Projects\noBSstatsdev`
   you need to use the following commands
   ```cmd
   cd Projects
   cd noBSstatsdev
   ```

2. Activate the Python virtual environment:
   ```cmd
   .venv\Scripts\activate.bat
   ```

3. Build the homepage 
   ```cmd
   python scripts/buildhomepage.py homepage
   ```

4. Run the deploy script:
   ```cmd
   python scripts/deploy.py homepage
   ```
   This will copy the contents of `homepage/dist/` to 
   `https://dev.noBSstats.com/homepage/`.
   On the first connection to an unknown server, the script will ask you to type `yes`
   to save the server key to `credentials/known_hosts`.
   Subsequent runs check the server key is the same,
   so you know you're connecting to the same server as on the first connection.


You can now view the uploaded HTML at https://dev.noBSstats.com/homepage/ 


You can use the deploy script to deploy other folders too.
To deploy the local folder `<folder>`, use the command
`python scripts/deploy.py <folder>`,
which will upload the HTML build content from the local `<folder>`
so that it gets served online at the public URL `https://dev.noBSstats.com/<folder>/`.








## Dev workflow

We'll use this code repo as a shared workspace for developing several versions
of the homepage noBSstats.com and the styles for the content pages.
- Use subfolders `<folder>` to store different versions of the Deliverable 1
  e.g. `homepage-v2`,  `homepage-v3`, etc., until  `homepage-final`,
  and similarly for deliverable 2  `styles-v1`,  `styles-v2`, `styles-v3`, until  `styles-final`.
- Each folder is completely independent, but easily sharable.
  For example, if you're working on the folder `homepage-demo` and you want to share it
  with the team, you can:
  - git add, commit, and push your local folder `homepage-demo` to the main repo 
  - git add, commit, and push local folder `homepage-demo` to a different branch, then open a pull request to the main branch
  - build your local folder `homepage-demo` and upload it to `https://dev.noBSstats.com/homepage-demo/`, then share this URL




## Links

- Dev website: https://dev.noBSstats.com/
  - See https://dev.noBSstats.com/homepage/ for sample homepage
  - See https://dev.noBSstats.com/sample/ for sample styles
- Dev website source repo: https://github.com/minireference/noBSstatsdev

