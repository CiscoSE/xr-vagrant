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
from ydk.models.cisco_ios_xr.Cisco_IOS_XR_ipv4_ospf_cfg import Ospf

if __name__ == "__main__":
    # create NETCONF session
    provider = NetconfServiceProvider(address="11.1.1.3",
                                      port=830,
                                      username="vagrant",
                                      password="vagrant",
                                      protocol="ssh")

    # create CRUD service
    crud = CRUDService()

    ospf = Ospf()

    ospf = crud.read(provider, ospf)

    for ospfProcess in ospf.processes.process:
        print "Process: " + ospfProcess.process_name
        for area in ospfProcess.default_vrf.area_addresses.area_area_id:
            print "Area: " + str(area.area_id)
            for interface in area.name_scopes.name_scope.keys():
                print "Interface: " + interface

    exit()
