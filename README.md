# Vagrant example for IOS XR
This repo contains a simple vagrant file that will create an IOS XRv 
and an Ubuntu virtual machine in order to use them as a development environment for YDK, gRPC or telemetry
 
## IOS XRv image

Download the vagrant image

https://xrdocs.io/application-hosting/tutorials/iosxr-vagrant-quickstart


## Create an XRv and a linux instance 

1) Clone the repository

```bash
git clone https://github.com/CiscoSE/xr-vagrant.git
```

2) Move to the root folder of the repo and start the VMs

```bash
vagrant up
```

You will see log messages with the ports that you will need to use to 
connect via ssh and netconf to the XRv:


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

In this example (keep in mind that when you bring the XRv up the port might be different),
port 22 of the router is mapped to port 2223 in your laptop. 
To login, use the port mapped to 22 (guest) with vagrant/vagrant credentials

ssh to the XRv using this command: (For Windows, use putty or another ssh client)

```bash
ssh vagrant@localhost -p 2223
```

XRv uses port 830 for netconf; it is mapped to 57779 in your laptop. If you want to run netconf calls to the XRv from
your laptop, 57779 is the port to use


The router.cfg file has a basic configuration for the XRv. Apply this configuration 
if you want to access the router from the linux VM. 


To login into the Linux VM use this command:

```bash
vagrant ssh devbox
```

YDK-py will be already installed and ready to use.
Access to the router from the Linux VM via 11.1.1.3 (remember to apply the router configuration in the previous step) 

Once you have connectivity to the XRv from this VM, you will be able to run the examples under ydk-examples directory.
 If you are running the examples from the VM, change the credentials and port in the code, since from the VM
  the netconf port will be 830 and IP 11.1.1.3
 
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
After configuring netconf in XRv, the ssh connection to port 830 will not work properly. Restart the router to fix the issue

```bash
vagrant halt -f rtr1
vagrant up rtr1
```

## Useful links

* YDK-Py: https://github.com/CiscoDevNet/ydk-py
* YDK-Py examples: https://github.com/CiscoDevNet/ydk-py-samples/tree/master/samples/basic/crud/models/cisco-ios-xr
* Tutorials and guides: https://xrdocs.io/

