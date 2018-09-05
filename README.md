# Vagrant example for IOS XR
This repo contains a simple vagrant file that will create an IOS XRv 
and an Ubuntu virtual machine in order to use them as a development environment for YDK, gRPC or telemetry
 
## IOS XRv image

To run XRv in your laptop you will need to download the image first.

https://xrdocs.io/application-hosting/tutorials/iosxr-vagrant-quickstart


## Create an XRv and a linux instance 

1) Clone this repository

```bash
git clone https://github.com/CiscoSE/xr-vagrant.git
```

2) Move to the root folder of the repo and start the VMs

```bash
vagrant up
```

You will see logs messages, including the ports that you will need to use to 
connect via ssh and netconf to XRv:


```bash
Bringing machine 'rtr1' up with 'virtualbox' provider...
(..)
==> rtr1: Forwarding ports...
    rtr1: 57722 (guest) => 2222 (host) (adapter 1)
    rtr1: 22 (guest) => 2223 (host) (adapter 1)
    rtr1: 57777 (guest) => 57778 (host) (adapter 1)
    rtr1: 830 (guest) => 57779 (host) (adapter 1)
(..)
```

In this example (when you bring your XRv up the port can be different)
port 22 of the router is mapped to port 2223 in your machine. 
To ssh to the router, use the port mapped to 22 (guest) with vagrant/vagrant credentials

You can ssh to the XRv using

```bash
ssh vagrant@localhost -p 2223
```

830 is the XRv netconf port; it is mapped to 57779 in your machine. Use port 57779 to redirect netconf calls 
to the router


The router.cfg file has a basic configuration for the XRv. Apply this configuration 
if you want to access the router from the linux VM. 


To login into the Linux VM use this command:

```bash
vagrant ssh devbox
```
This is an Ubuntu VM with YDK-py installed and ready to use!
Access to the router from the Linux VM via 11.1.1.3 (after you apply the router configuration in the previous step) 

Once you have connectivity to the router from this VM, you will be able to execute the examples.
 Remember to change the credentials and port, since from the VM the netconf port will be 830 and IP 11.1.1.3
 
```python
provider = NetconfServiceProvider(address="11.1.1.3",
                                  port=830,
                                  username="vagrant",
                                  password="vagrant",
                                  protocol="ssh")
```


3) If you need to remove the VMs 


```bash
vagrant destroy
```


## Known issues
If you configure netconf in the router, you will need to restart the router using the
 following commands

```bash
vagrant halt -f rtr1
vagrant up rtr1
```

## Examples and tutorials
There are a couple of python examples under ydk-examples directory. In order to run them, be sure the 
install the yang development kit: https://github.com/CiscoDevNet/ydk-py
More examples can be found at https://github.com/CiscoDevNet/ydk-py-samples/tree/master/samples/basic/crud/models/cisco-ios-xr

Tutorials at https://xrdocs.io/

