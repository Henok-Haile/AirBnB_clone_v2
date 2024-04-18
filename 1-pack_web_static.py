#!/usr/bin/python3
# A Fabric script that generates a .tgz archive from the contents of
# the web_static folder

from fabric.api import local
import time
import os


def do_pack():
    """Creates a tar gziiped archive of the folder of the web_static."""
    try:
        local("mkdir -p versions")
        now = time.strftime("%Y%m%d%H%M%S")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".format(now))
        file_size = os.path.getsize("versions/web_static_{}.tgz".format(now))
        print(f"web_static packed: versions/web_static_{now}.tgz -> {file_size}Bytes")
        return ("versions/web_static_{}.tgz".format(now))
    except:
        return None
        
