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

2) Move to the root folder of the repo and start the VM

```bash
vagrant up
```

3) If you need to remove the VM 


```bash
vagrant destroy
```


## Known issues
If you configure netconf in the router, you will need to restart the router using the
 following commands

```bash
vagrant halt -f
vagrant up
```

## Examples and tutorials
There are a couple of python examples under ydk-examples directory. In order to run them, be sure the 
install the yang development kit: https://github.com/CiscoDevNet/ydk-py

More tutorials at https://xrdocs.io/

