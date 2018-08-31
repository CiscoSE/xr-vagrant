"""
Copyright (c) 2018 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""
from ydk.services import CRUDService
from ydk.providers import NetconfServiceProvider
from ydk.models.cisco_ios_xr.Cisco_IOS_XR_ifmgr_cfg import InterfaceConfigurations

if __name__ == "__main__":
    # create NETCONF session
    provider = NetconfServiceProvider(address="localhost",
                                      port=57779,
                                      username="vagrant",
                                      password="vagrant",
                                      protocol="ssh")


    # create CRUD service
    crud = CRUDService()

    # create interface config object
    interfacesDef = InterfaceConfigurations()

    # read system time from device
    interfaces = crud.read(provider, interfacesDef)

    for interfaceConfig in interfaces.interface_configuration:
        if interfaceConfig.interface_name == "GigabitEthernet0/0/0/0":
            interfaceConfig.description = "Changed from YDK"
            break

    if crud.update(provider, interfaces):
        print "Changed!"



    exit()
