#!/bin/sh

# Update dependencies
sudo apt-get update

# Install firefox browser
sudo apt-get install -y firefox-esr

# Install Python and pip
sudo apt-get install -y python3 python3-pip


pip3 install --upgrade -r requirements.txt