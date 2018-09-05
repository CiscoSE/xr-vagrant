#!/bin/sh

sudo apt-get update
sudo apt-get install python-minimal -y
sudo apt-get install gdebi-core python3-dev python-dev libtool-bin -y
wget https://devhub.cisco.com/artifactory/debian-ydk/0.7.2/libydk_0.7.2-1_amd64.deb
sudo gdebi libydk_0.7.2-1_amd64.deb -n
sudo apt-get install python-pip -y

pip install pybind11
pip install ydk
pip install ydk-models-cisco-ios-xr
git clone https://github.com/CiscoSE/xr-vagrant.git

