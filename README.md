# Vagrant lab for IOS XR
This repo contains a simple vagrant file that will create an IOS XRv 
and an Ubuntu virtual machine in order to use them as a development environment for YDK, gRPC or telemetry

The lab assumes that you have vagrant, virtual box and an XRv image in your laptop

## Step 1 - Create an XRv and a linux instance 

Clone the repository

```bash
git clone https://github.com/CiscoSE/xr-vagrant.git
```

Move to the root folder of the repo and start the VMs

```bash
vagrant up
```

You will see log messages with the ports that you will need to use to 
connect via ssh and netconf to the XRv.

Congratulations! You have an XRv and a linux VM up and running in your laptop

## Step 2 - Assign initial config to the XRv
 
To login into the router, you will need to check the port that is mapped to the ssh port of the XRv.
Execute this commands to get that information

```bash
vagrant port rtr1
```

The output will look like this:
```bash
$ vagrant port rtr1

The forwarded ports for the machine are listed below. Please note that
these values may differ from values configured in the Vagrantfile if the
provider supports automatic port collision detection and resolution.

 57777 (guest) => 57778 (host)
   830 (guest) => 57779 (host)
    22 (guest) => 2223 (host)
 57722 (guest) => 2200 (host)
```
For this XRv instance, XRv's port 22 is mapped to 2223 (keep in mind that in your laptop this port might be different)

Login into the router using the following command: (if using windows, putty or another ssh client will work)
```bash
ssh vagrant@localhost -p 2223
```
Password is _vagrant_

Apply the configuration located in this file: https://github.com/CiscoSE/xr-vagrant/blob/master/router.cfg

After configuring netconf in XRv, the ssh connection to port 830 will not work properly. Restart the router to fix the issue

```bash
vagrant halt -f rtr1
vagrant up rtr1
```

## Step 3 - Configure BGP from the Ubuntu VM using YDK

There are six scripts under the ydk-examples directory included in this repo. This examples are already located
in the ubuntu VM. 

Login into the VM:
```bash
vagrant ssh devbox
```

Go to the directory where the examples are located

```bash
cd /home/vagrant/xr-vagrant/ydk-examples
```

Execute the createBgpCfg.py script. You can see the code that will get executed here: https://github.com/CiscoSE/xr-vagrant/blob/master/ydk-examples/createBgpCfg.py

```bash
python createBgpCfg.py
```

Login into the router using the following command: (if using windows, putty or another ssh client will work)
```bash
ssh vagrant@localhost -p 2223
```
Password is _vagrant_

Issuing a _show running router bgp_ will show the new configuration added

```bash
RP/0/RP0/CPU0:rtr1#show running-config router bgp 
Thu Sep  6 09:39:33.104 UTC
router bgp 65001
 address-family ipv4 unicast
 !
 neighbor-group IBGP
  remote-as 65001
  update-source Loopback0
  address-family ipv4 unicast
  !
 !
 neighbor 172.16.255.2
  use neighbor-group IBGP
 !
!
```

## Step 4 - Read BGP configuration from the Ubuntu VM using YDK

We are going to read the configuration that we just applied using YDK. From the same directory, execute the readBgpCfg.py file

```bash
python readBgpCfg.py
```

You can see the code that is executed here: https://github.com/CiscoSE/xr-vagrant/blob/master/ydk-examples/readBgpCfg.py

The output will look like this
```bash
vagrant@ubuntu-xenial:~/xr-vagrant/ydk-examples$ python readBgpCfg.py 
AS 65001
	 Neighbor 172.16.255.2
		IBGP
```


## Step 5 - Write and read OSPF configuration from the Ubuntu VM using YDK

From the same directory, execute the createOpsfCfg.py file. You can see the code here https://github.com/CiscoSE/xr-vagrant/blob/master/ydk-examples/createOspfCfg.py

```bash
python createOspfCfg.py
```
Source code of this script can be found here: https://github.com/CiscoSE/xr-vagrant/blob/master/ydk-examples/createOspfCfg.py

From the router, run a _show running router ospf_ to see the new configuration

```bash
RP/0/RP0/CPU0:rtr1#show running-config router ospf
Thu Sep  6 10:13:04.926 UTC
router ospf DEFAULT
 router-id 172.16.255.1
 area 0
  interface GigabitEthernet0/0/0/0
   network point-to-point
  !
 !
 area 1
  interface GigabitEthernet0/0/0/1
   network point-to-point
  !
 !
!
```

From the ubuntu VM, read the configuration using the readOspfCfg.py script
```bash
python readOspfCfg.py
```
Source code of the script is located at https://github.com/CiscoSE/xr-vagrant/blob/master/ydk-examples/createOspfCfg.py

The result will look like this:

```bash
vagrant@ubuntu-xenial:~/xr-vagrant/ydk-examples$ python readOspfCfg.py 
Process: DEFAULT
Area: 0
Interface: GigabitEthernet0/0/0/0
Area: 1
Interface: GigabitEthernet0/0/0/1
```

## Step 7 - Changing from the Ubuntu VM using YDK

The updateIfDescription.py file will change the description on interface _GigabitEthernet0/0/0/0_ to _Changed from YDK_

From the same directory, run the script. (Source code at https://github.com/CiscoSE/xr-vagrant/blob/master/ydk-examples/updateIfDescription.py)

```bash
python updateIfDescription.py
```

After it finishes, check the interface configuration on the router:

```bash
RP/0/RP0/CPU0:rtr1#show running-config interface GigabitEthernet 0/0/0/0 
Thu Sep  6 10:21:21.326 UTC
interface GigabitEthernet0/0/0/0
 description Changed from YDK
 shutdown
!
```

## Step 8 - Reading operational data from the Ubuntu VM using YDK

Besides changing and reading configurations, YDK can be used to read operational data such as router up time.

In the same directory, run the readUpTime.py script. If you are interested, here is the code: https://github.com/CiscoSE/xr-vagrant/blob/master/ydk-examples/readUpTime.py)

```bash
python readUpTime.py
```

The result will look like this:

```bash
vagrant@ubuntu-xenial:~/xr-vagrant/ydk-examples$ python readUpTime.py 
System uptime is 15:26:47
```

## Bonus: Installing the Advanced Netconf Explorer

ANX (Advanced Netconf Explorer) is a graphical explorer for NETCONF / YANG and GNMI/GRPC Telemetry & Java NETCONF 1.1 client library

You can find more information at https://github.com/cisco-ie/anx

In this section, we are going to install the explorer on top of the ubuntu VM.
Execute the following commands

```
sudo apt-get install docker.io -y
git clone https://github.com/cisco-ie/anx.git
cd anx
sudo docker build -t netconf-explorer .
sudo docker run --name netconf-exlorer -d -p 9269:8080 netconf-explorer
```

In order to access to the web user interface, you will need to map the port that anx is using in the VM to the laptop: 

1) Open virtual box  
2) Select the devbox VM
3) Go to settings
4) Select Network
5) Advanced -> Port forwarding

Add an entry with the following information:
Name: anx
Protocol: TCP
Host IP: 127.0.0.1
Host port: 8080
Guest IP: Leave this one blank
Guest Port: 9269

Go to http://127.0.0.1:8080/ and connect to the router using IP 11.1.1.3 and vagrant/vagrant credentials


## Useful links

* YDK-Py: https://github.com/CiscoDevNet/ydk-py
* YDK-Py examples: https://github.com/CiscoDevNet/ydk-py-samples/tree/master/samples/basic/crud/models/cisco-ios-xr
* Tutorials and guides: https://xrdocs.io/
* ANX: https://github.com/cisco-ie/anx
* Telemetry tutorial: https://xrdocs.io/programmability/tutorials/2017-08-14-validate-the-intent-of-network-config-changes/
