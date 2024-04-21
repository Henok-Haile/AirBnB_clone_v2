#!/usr/bin/python3
""" A Fabric script (based on the file 1-pack_web_static.py)
 that distributes an archive to the web servers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.198.54.29', '54.165.42.234']


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        file_nm = archive_path.split("/")[-1]
        arc_nm = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, arc_nm))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_nm, path, arc_nm))
        run('rm /tmp/{}'.format(file_nm))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, arc_nm))
        run('rm -rf {}{}/web_static'.format(path, arc_nm))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, arc_nm))
        print("New version deployed!")
        return True
    except:
        return False
