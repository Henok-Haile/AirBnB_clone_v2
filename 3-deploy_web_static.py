#!/usr/bin/python3
"""
Fabric script for deploying a web application.
"""

from fabric.api import local, run, put, env
from datetime import datetime
import os

env.hosts = ["100.25.47.158", "35.153.193.110"]


def do_pack():
    """
    Creates a compressed archive of the web_static folder.

    Returns:
        str: Path to the created archive file.
    """
    try:
        if not os.path.exists("web_static"):
            print("Error: 'web_static' folder does not exist.")
            return None

        # Create the 'versions' directory if it doesn't exist
        if not os.path.exists("versions"):
            os.makedirs("versions")

        date = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))

        # Get the file size
        file_size = os.path.getsize(file_name)

        print(f"web_static packed: {file_name} -> {file_size}Bytes")
        return file_name
    except Exception as e:
        print("An error occurred while creating the archive:", e)
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.

    Args:
        archive_path (str): Path to the archive file to be deployed.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    if not os.path.exists(archive_path):
        print(f"Error: Archive {archive_path} not found.")
        return False
    try:
        file_name = os.path.basename(archive_path)
        arc_name = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, arc_name))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, arc_name))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, arc_name))
        run('rm -rf {}{}/web_static'.format(path, arc_name))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, arc_name))
        print("New version deployed!")
        return True
    except Exception as e:
        print("An error occurred while deploying the archive:", e)
        return False


def deploy():
    """
    Create and distribute an archive to the web servers.

    Returns:
        bool: True if deployment was successful, False otherwise.
    """
    try:
        file = do_pack()
        if file is None:
            return False
        return do_deploy(file)
    except Exception as e:
        print("An error occurred during deployment:", e)
        return False


if __name__ == "__main__":
    deploy()

