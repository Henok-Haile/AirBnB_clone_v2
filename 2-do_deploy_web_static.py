#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from fabric.api import put, run, env
import os
env.hosts = ['54.198.54.29', '54.165.42.234']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        archive_name = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}{}/'.format(path, archive_name))
        run('sudo tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, archive_name))
        run('sudo rm /tmp/{}'.format(file_name))
        run('sudo mv {0}{1}/web_static/* {0}{1}/'.format(path, archive_name))
        run('sudo rm -rf {}{}/web_static'.format(path, archive_name))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {}{}/ /data/web_static/current'.format(path, archive_name))
        print("New version deployed!")
        return True
    except:
        return False
