#!/usr/bin/python3
# A Fabric script (based on the file 1-pack_web_static.py)
# that distributes an archive to the web servers

import os
from fabric.api import run, env, put

env.hosts = ["54.198.54.29", "54.165.42.234"]


def do_deploy(archive_path):
    """Distributes an archive to your web servers.

    Args:
        archive_path (str): The path of the archive to distribute.
    Returns:
        False if the file at the path archive_path doesn’t exist else True.
    """
    if os.path.exists(archive_path) is False:
        return False

    try:
        archive = archive_path.split("/")[-1]
        archive_name = archive.split(".")[0]
        path = "/data/web_static/releases/"

        put(archive_path, '/tmp/')
        run('mkdir -p {}{}'.format(path, archive_name))
        run('tar -xzf /tmp/{} -C {}{}'.format(archive, path, archive_name))
        run('rm /tmp/{}'.format(archive))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, archive_name))
        run('rm -rf {}{}/web_static'.format(path, archive_name))
        run('rm -rf /data/web_stattic/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, archive_name))
        return True
    except:
        return false
