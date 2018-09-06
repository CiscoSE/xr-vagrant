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
from ydk.models.cisco_ios_xr.Cisco_IOS_XR_ipv4_bgp_cfg import Bgp

if __name__ == "__main__":
    # create NETCONF session
    provider = NetconfServiceProvider(address="11.1.1.3",
                                      port=830,
                                      username="vagrant",
                                      password="vagrant",
                                      protocol="ssh")

    # create CRUD service
    crud = CRUDService()

    bgp = Bgp()

    bgp = crud.read(provider, bgp)

    for instance in bgp.instance["default"].instance_as:
        for fourByteAs in instance.four_byte_as:
            print("AS " + str(fourByteAs.as_))
            for neighbor in fourByteAs.default_vrf.bgp_entity.neighbors.neighbor:
                print "\t Neighbor " + neighbor.neighbor_address
                print "\t\t" + neighbor.neighbor_group_add_member

    exit()
