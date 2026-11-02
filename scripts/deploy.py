#!/usr/bin/env python3
"""Upload <folder>/dist/ or <folder>/_build/html/ to WEBROOT/<folder>/."""

import argparse
import getpass
import os
import posixpath
import re
from urllib.parse import urljoin

import paramiko


# Project settings: edit these once for your server.
SSH_HOST = "dev.noBSstats.com"
SSH_USER = "admin"
SSH_PORT = 22
SSH_PRIVATE_KEY = "credentials/admin_key"  # Private key, not id_rsa.pub.
SSH_KNOWN_HOSTS = "credentials/known_hosts"

WEBROOT = "/var/www/html"
WEBROOT_URL = "https://dev.noBSstats.com/"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


VERBOSE = False

class ConfirmHostKey(paramiko.MissingHostKeyPolicy):
    """Confirm and save a new server key, as an SSH client normally does."""

    def missing_host_key(self, client, hostname, key):
        print("Server:", hostname)
        print("Host key:", key.get_name(), key.fingerprint)
        answer = input("Trust this host key and save it? Type yes: ")
        if answer.strip().lower() != "yes":
            raise paramiko.SSHException("Host key was not trusted.")
        client.get_host_keys().add(hostname, key.get_name(), key)
        filename = os.path.join(ROOT, SSH_KNOWN_HOSTS)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        client.save_host_keys(filename)


def make_directory(sftp, path):
    """Create a remote directory and any missing parents."""
    try:
        sftp.stat(path)
    except FileNotFoundError:
        make_directory(sftp, posixpath.dirname(path))
        sftp.mkdir(path, mode=0o755)


def upload_directory(sftp, local, remote, deploy_type):
    """Copy every file, including dotfiles and nested directories."""
    make_directory(sftp, remote)
    for name in sorted(os.listdir(local)):
        source = os.path.join(local, name)
        target = posixpath.join(remote, name)
        if os.path.isdir(source):
            upload_directory(sftp, source, target, deploy_type)
        else:
            sftp.put(source, target)
            if deploy_type == "homepage" or VERBOSE:
                print("Uploaded:", target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="Site folder, for example: sample or homepage")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", args.folder):
        parser.error("Use a single folder name such as sample or homepage.")
    if not posixpath.isabs(WEBROOT):
        parser.error("WEBROOT must be an absolute server path.")


    directory = os.path.join(ROOT, args.folder)


    # Detmine what kind of deploy this is: homepage or styles
    # and set `local` directory whose contents we want to deploy
    homepageassets_dir = os.path.join(directory, "homepageassets")
    myst_file = os.path.join(directory, "myst.yml")
    deploy_type = None
    if os.path.isdir(homepageassets_dir):
        deploy_type = "homepage"
        local = os.path.join(directory, "dist")
        builder = "buildhomepage.py"
    elif os.path.isfile(myst_file):
        deploy_type = "styles"
        local = os.path.join(directory, "_build", "html")
        builder = "build.py"
    else:
        raise ValueError("Didn't find neither hoempageassets/ nor myst.yml so qitting...")

    # 
    print("Deploy type", deploy_type)

    # Check that the local folder we want to deploy contains an index.html
    if not os.path.isfile(os.path.join(local, "index.html")):
        parser.error(
            "No index.html in " + local + ". Build first: python scripts/"
            + builder + " " + args.folder
        )

    # Destination where we're uploaing to on the web server
    remote = posixpath.join(WEBROOT, args.folder)

    # Credentials we'll use to connect to the web server
    key_file = os.path.join(ROOT, SSH_PRIVATE_KEY)
    known_hosts = os.path.join(ROOT, SSH_KNOWN_HOSTS)

    try:
        try:
            # This assumes ssh key is in either RSA, Ed25519, or ECDSA format
            key = paramiko.PKey.from_path(key_file)
        except TypeError:
            # If ssh private key is password-protected, prompt the user for the password
            password = getpass.getpass("Private-key passphrase: ")
            key = paramiko.PKey.from_path(key_file, password=password.encode("utf-8"))

        with paramiko.SSHClient() as client:
            client.load_system_host_keys()
            if os.path.isfile(known_hosts):
                client.load_host_keys(known_hosts)
            client.set_missing_host_key_policy(ConfirmHostKey())
            client.connect(
                SSH_HOST, port=SSH_PORT, username=SSH_USER, pkey=key,
                allow_agent=False, look_for_keys=False, timeout=15,
                banner_timeout=15, auth_timeout=30,
            )
            print(f"Starting deploy {local} to https://dev.noBSstats.com/{args.folder}/")
            if deploy_type == "styles":
                print("We're uploading thousands of tiny files so upload might take a few minutes.")
            with client.open_sftp() as sftp:
                sftp.get_channel().settimeout(60)
                print("Uploading:", local)
                upload_directory(sftp, local, remote, deploy_type)
        print("Deployed to", remote + "/")
        print("See ", urljoin(WEBROOT_URL, args.folder + "/"), "to view the live version.")

    except (OSError, ValueError, TypeError, EOFError, paramiko.SSHException) as error:
        parser.exit(1, "Error: " + (str(error) or type(error).__name__) + "\n")
    except KeyboardInterrupt:
        parser.exit(130, "\nDeployment interrupted.\n")


if __name__ == "__main__":
    main()
