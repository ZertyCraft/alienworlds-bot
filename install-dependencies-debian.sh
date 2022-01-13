#!/bin/sh

# Update dependencies
sudo apt-get update

# Install firefox browser
sudo apt-get install -y firefox-esr

# Install Geckodriver
wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.30.0-linux64.tar.gz
tar -xvzf geckodriver-v0.30.0-linux64.tar.gz
chmod +x geckodriver
mv geckodriver /usr/local/bin/


# Install Python and pip
sudo apt-get install -y python3 python3-pip


pip3 install --upgrade -r requirements.txt
