#!/usr/bin/python3
# A Fabric script (based on the file 1-pack_web_static.py)
# that distributes an archive to the web servers

import os
from fabric.api import run, env, put

env.hosts = ["54.198.54.29", "54.165.42.234"]


def do_pack():
    """Creates a tar gziiped archive of the folder of the web_static."""
    try:
        if not os.path.exists("web_static"):
            print("Error: 'web_static' folder does not exist.")
            return None

        # Create the 'versions' directory if it doesn't exist
        local("sudo mkdir -p versions")

        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))

        # Get the file size
        file_size = os.path.getsize(file_name)

        print(f"web_static packed: {file_name} -> {file_size}Bytes")
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        False if the file at the path archive_path doesn’t exist else True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("sudo mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("sudo rm /tmp/{}".format(file)).failed is True:
        return False
    if run("sudo mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("sudo rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("sudo rm -rf /data/web_static/current").failed is True:
        return False
    if run("sudo ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    return True
