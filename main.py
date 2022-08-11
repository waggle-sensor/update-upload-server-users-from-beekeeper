#!/usr/bin/env python3
import os
from pathlib import Path
import requests
import subprocess


BEEKEEPER_STATE_ENDPOINT = os.environ["BEEKEEPER_STATE_ENDPOINT"]
BEEHIVE_NAME = os.environ["BEEHIVE_NAME"]
UPLOAD_SERVER_HOST = os.environ["UPLOAD_SERVER_HOST"]
UPLOAD_SERVER_PORT = os.environ["UPLOAD_SERVER_PORT"]
UPLOAD_SERVER_USER = os.environ["UPLOAD_SERVER_USER"]
UPLOAD_SERVER_KEY = os.environ["UPLOAD_SERVER_KEY"]


def get_node_users_for_beehive():
    r = requests.get(BEEKEEPER_STATE_ENDPOINT)
    r.raise_for_status()
    items = r.json()["data"]
    return {"node-"+item["id"].lower() for item in items if item["beehive"] == BEEHIVE_NAME}


def main():
    want_users = get_node_users_for_beehive()

    ssh_args = [
        f"{UPLOAD_SERVER_USER}@{UPLOAD_SERVER_HOST}",
        "-p",
        str(UPLOAD_SERVER_PORT),
        "-i",
        Path(UPLOAD_SERVER_KEY).absolute(),
    ]

    output = subprocess.check_output(["ssh", *ssh_args, "cat", "/etc/passwd"], text=True)

    has_users = {user for user in map(lambda s: s.split(":")[0], output.splitlines()) if user.startswith("node-")}
    add_users = want_users - has_users
    del_users = has_users - want_users

    script = ""

    for user in sorted(add_users):
        script += f"sudo bk-add-user '{user}'\n"

    for user in sorted(del_users):
        script += f"sudo bk-del-user '{user}'\n"

    print("has:", sorted(want_users))
    print("has:", sorted(has_users))
    print("add:", sorted(add_users))
    print("del:", sorted(del_users))

    if script:
        subprocess.run(["ssh", *ssh_args, "sh", "-"], input=script.encode(), check=True)


if __name__ == "__main__":
    main()
