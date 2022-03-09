#!/bin/bash
#
# Download this file into the home directory of the device. 
# Give this file execution rights (chmod +x setup.sh)
# Then execute this file (./setup.sh)

###############
# BOILERPLATE #
###############

# https://stackoverflow.com/a/5947802/7254995
printRed () {
    echo -e "\033[0;31m$1\033[0m"
}
printBlue () {
    echo -e "\033[1;34m$1\033[0m"
}
printGreen () {
    echo -e "\033[1;32m$1\033[0m"
}

set -e
set -o pipefail
exitingDueToError() {
    printRed "ERROR: Setup did not succeed."
} 
trap exitingDueToError ERR


######################################
# IF SETUP IS NOT RUN THE FIRST TIME #
######################################

# || true prevents tripping our set -e setting. If these fail, it's ok.
sudo systemctl stop gunicorn.socket || true
sudo systemctl disable gunicorn.socket || true
sudo systemctl stop nginx || true


#####################
# SETUP /deltaForce #
#####################

if [[ ! -e /deltaForce ]]
then
    sudo mkdir /deltaForce
    printGreen "Successfully created /deltaForce"
else 
    sudo rm -rf /deltaForce
    printGreen "/deltaForce already existed; deleting everything"
    sudo mkdir /deltaForce
    printGreen "Successfully recreated /deltaForce"
fi

cd /deltaForce


################
# DEPENDENCIES #
################

# Install dependencies if not already installed
sudo apt install -y --upgrade git python3 python3-distutils
printGreen "Successfully (re)installed dependencies"

# Install nginx
# https://nginx.org/en/linux_packages.html#Debian
if [[ -z "$(which nginx)" ]]
then
    sudo apt install -y --upgrade curl gnupg2 ca-certificates lsb-release debian-archive-keyring
    curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
    checksum=$(echo $(gpg --dry-run --quiet --import --import-options import-show /usr/share/keyrings/nginx-archive-keyring.gpg))
    correctChecksum=$(echo "pub rsa2048 2011-08-19 [SC] [expires: 2024-06-14] 573BFD6B3D8FBC641079A6ABABF5BD827BD9BF62 uid nginx signing key <signing-key@nginx.com>")
    if [[ "$checksum" != "$correctChecksum" ]]
    then
        printRed "NGINX installation failed: unexpected checksum"
        exit 1
    fi
    echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] http://nginx.org/packages/debian `lsb_release -cs` nginx" | sudo tee /etc/apt/sources.list.d/nginx.list
    echo -e "Package: *\nPin: origin nginx.org\nPin: release o=nginx\nPin-Priority: 900\n" | sudo tee /etc/apt/preferences.d/99nginx
    sudo apt update
    sudo apt install -y nginx
    printGreen "Successfully installed NGINX"
else
    sudo apt update
    sudo apt install -y --upgrade nginx
    printGreen "Successfully upgraded NGINX"
fi

# Install pip if not already installed
if [[ -z "$(which pip)" ]]
then
    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    if [[ "$PATH" != *"$(dirname $(which pip))"* ]] # if parent directory of pip not in PATH
    then
        echo 'export PATH="/home/pi/.local/bin:$PATH"' >> ~/.bashrc
        source ~/.bashrc
    fi
    rm get-pip.py
    printGreen "Successfully installed pip"
else
    printGreen "pip already installed"
    pip install --upgrade pip
    printGreen "Successfully upgraded pip"
fi


#############
# GIT CLONE #
#############

git clone -b deployment-server --single-branch https://github.com/Marchhill/exhibition-inference.git
printGreen "Successfully cloned exhibition-inference github repository"

GITHUB_BASE_DIR="/deltaForce/exhibition-inference/"
cd exhibition-inference
pip install -r requirements.txt
printGreen "Successfully installed exhibition-inference pip dependencies"

python3 site/exhibitionInferenceSite/manage.py collectstatic  # Collect static files


#################
# SYSTEMD SETUP #
#################

sudo cat <<EOF > /etc/systemd/system/gunicorn.socket
[Unit]
Description=delta force gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

sudo cat <<EOF > /etc/systemd/system/gunicorn.service
[Unit]
Description=delta force gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$(whoami)
Group=www-data
WorkingDirectory=${GITHUB_BASE_DIR}site/exhibitionInferenceSite
ExecStart=$(which gunicorn) \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          exhibitionInferenceSite.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

sudo cat <<EOF > /etc/nginx/nginx.conf
user $(whoami);
worker_processes  auto;

error_log  /var/log/nginx/error.log notice;
pid        /var/run/nginx.pid;


events {
    worker_connections  1024;
}


http {
    server {
        listen 80;

        # Ignore problems related to finding favicon
        location = /favicon.ico {
            access_log off; 
            log_not_found off;
        }
        location /static/ {
            autoindex on;
            alias ${GITHUB_BASE_DIR}site/exhibitionInferenceSite/static_root/;
        }
        location / {
            proxy_pass http://unix:/run/gunicorn.sock;
            proxy_set_header    Host $host;
        }
    }
}
EOF

sudo systemctl daemon-reload
printGreen "Successfully wrote and reloaded gunicorn & nginx configuration files for systemd"

sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl start nginx

printGreen "Successfully started gunicorn and nginx"


########
# DONE #
########

echo
printGreen "Installation success :) Server is up and running."