#!/usr/bin/python3
# A Fabric script that generates a .tgz archive from the contents of
# the web_static folder

from fabric.api import local
import time


def do_pack():
    """Creates a tar gziiped archive of the folder of the web_static."""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return ("versions/web_static_{}.tgz".format(time.
                strftime("%Y%m%d%H%M%S")))
    except:
        return None
