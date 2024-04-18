#!/usr/bin/env bash
# A bash script that sets up your web servers for the deployment of web_static
sudo apt-get update
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

sudo echo "Cohort 19 ALX School student" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/listen 80 default_server/a \\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}' /etc/nginx/sites-available/default

sudo service nginx restart
