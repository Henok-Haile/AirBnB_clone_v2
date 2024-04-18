#!/usr/bin/python3
# A Fabric script that generates a .tgz archive from the contents of
# the web_static folder

from fabric.api import local
from datetime import datetime
import os

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

