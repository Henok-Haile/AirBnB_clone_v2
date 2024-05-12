#!/usr/bin/python3
# A Fabric script (based on the file 2-do_deploy_web_static.py) that creates
# and distributes an archive to your web servers, using the function deploy

from fabric.api import local, run, put, env
from datetime import datetime
import os

env.hosts = ["100.25.47.158", "35.153.193.110"]


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
        print(file_name)
        return file_name
    except:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if os.path.exists(archive_path) is False:
        return False
    try:
        file_nm = archive_path.split("/")[-1]
        arc_nm = file_nm.split(".")[0]
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


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
