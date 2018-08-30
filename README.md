# Vagrant example for IOS XR
This repo contains a simple vagrant file that will create an IOS XRv virtual machine
and map grpc and netconf ports in order to use it as a development environment
 
## IOS XRv image

In order to run XRv in your laptop you will need to download the image first.

https://xrdocs.io/application-hosting/tutorials/iosxr-vagrant-quickstart


## Create an XRv instance

1) Clone this repository

```bash
git clone https://github.com/CiscoSE/xr-vagrant.git
```

2) Move to the root folder of the repo and install pip dependencies (use a virtual environment when possible)

```bash
pip install -r requirements.txt
```

3) Start the VM

```bash
vagrant up
```

4) If you need to remove the VM 


```bash
vagrant destroy
```

There are a couple of python examples under ydk-examples directory

More tutorials at https://xrdocs.io/
