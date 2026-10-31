#!/usr/bin/env python3
"""Upload <folder>/_build/html/ to WEBROOT/<folder>/ using Python SFTP."""

import argparse
import getpass
import os
import posixpath
import re

import paramiko


# Project settings: edit these once for your server.
SSH_HOST = "your-server.example.com"
SSH_USER = "your-ssh-user"
SSH_PORT = 22
SSH_PRIVATE_KEY = "credentials/id_rsa"  # Private key, not id_rsa.pub.
SSH_KNOWN_HOSTS = "credentials/known_hosts"
WEBROOT = "/var/www/html"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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


def upload_directory(sftp, local, remote):
    """Copy every file, including dotfiles and nested directories."""
    make_directory(sftp, remote)
    for name in sorted(os.listdir(local)):
        source = os.path.join(local, name)
        target = posixpath.join(remote, name)
        if os.path.isdir(source):
            upload_directory(sftp, source, target)
        else:
            sftp.put(source, target)
            print("Uploaded:", target)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", help="Book folder, for example: sample")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]*", args.folder):
        parser.error("Use a single folder name such as sample or design-v2.")
    if not posixpath.isabs(WEBROOT):
        parser.error("WEBROOT must be an absolute server path.")

    local = os.path.join(ROOT, args.folder, "_build", "html")
    if not os.path.isfile(os.path.join(local, "index.html")):
        parser.error("Build first: python scripts/build.py " + args.folder)
    remote = posixpath.join(WEBROOT, args.folder)
    key_file = os.path.join(ROOT, SSH_PRIVATE_KEY)
    known_hosts = os.path.join(ROOT, SSH_KNOWN_HOSTS)

    try:
        # from_path detects RSA, Ed25519, or ECDSA private keys.
        try:
            key = paramiko.PKey.from_path(key_file)
        except TypeError:
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
            with client.open_sftp() as sftp:
                sftp.get_channel().settimeout(60)
                upload_directory(sftp, local, remote)
        print("Deployed to", remote + "/")
    except (OSError, ValueError, TypeError, EOFError, paramiko.SSHException) as error:
        parser.exit(1, "Error: " + (str(error) or type(error).__name__) + "\n")
    except KeyboardInterrupt:
        parser.exit(130, "\nDeployment interrupted.\n")


if __name__ == "__main__":
    main()
