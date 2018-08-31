# -*- mode: ruby -*-

# vi: set ft=ruby :

Vagrant.configure(2) do |config|

    config.vm.define "rtr1" do |node|
      node.vm.box =  "IOS-XRv"

      # Forward a port for grpc server access from the host, for eg. port 57777 configured on XR, forwarded to 57778 on host
      node.vm.network :forwarded_port, guest: 57777, host: 57778, id: "grpc", auto_correct: true

      # Forward a port for netconf server access from the host, for eg. port 830 configured on XR, forwarded to 57779 on host
      node.vm.network :forwarded_port, guest: 830, host: 57779, id: "netconf", auto_correct: true

      # gig0/0/0/0 connected to link1, gig00/0/1 connected to link2, gig0/0/0/2 connected to link3, auto-config not supported.
      node.vm.network :private_network, virtualbox__intnet: "link1", auto_config: false
      node.vm.network :private_network, virtualbox__intnet: "link2", auto_config: false
      node.vm.network :private_network, virtualbox__intnet: "link3", auto_config: false

    end

    config.vm.define "devbox" do |node|
      node.vm.box =  "ubuntu/xenial64"

      # eth1 connected to link2, auto_config is supported for an ubuntu instance
      node.vm.network :private_network, virtualbox__intnet: "link2", ip: "11.1.1.2"
    end
end