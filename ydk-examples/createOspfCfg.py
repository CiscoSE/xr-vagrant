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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_ospf_cfg \
    as xr_ipv4_ospf_cfg
from ydk.types import Empty


def config_ospf(ospf):
    """Add config data to ospf object."""
    # OSPF process
    process = ospf.processes.Process()
    process.process_name = "DEFAULT"
    process.default_vrf.router_id = "1.1.1.1"
    process.start = Empty()

    # Area 0
    area_area_id = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id.area_id = 0
    area_area_id.running = Empty()

    # gi0/0/0/0 interface
    name_scope = area_area_id.name_scopes.NameScope()
    name_scope.interface_name = "GigabitEthernet0/0/0/0"
    name_scope.running = Empty()
    name_scope.network_type = xr_ipv4_ospf_cfg.OspfNetwork.point_to_point
    area_area_id.name_scopes.name_scope.append(name_scope)

    # Area 1
    area_area_id_1 = process.default_vrf.area_addresses.AreaAreaId()
    area_area_id_1.area_id = 1
    area_area_id_1.running = Empty()

    # gi0/0/0/1 interface
    name_scope_g1 = area_area_id.name_scopes.NameScope()
    name_scope_g1.interface_name = "GigabitEthernet0/0/0/1"
    name_scope_g1.running = Empty()
    name_scope_g1.network_type = xr_ipv4_ospf_cfg.OspfNetwork.point_to_point
    area_area_id_1.name_scopes.name_scope.append(name_scope_g1)

    # append area/process config
    process.default_vrf.area_addresses.area_area_id.append(area_area_id)
    process.default_vrf.area_addresses.area_area_id.append(area_area_id_1)
    ospf.processes.process.append(process)


if __name__ == "__main__":
    """Execute main program."""

    # create NETCONF provider
    provider = NetconfServiceProvider(address="11.1.1.3",
                                      port=830,
                                      username="vagrant",
                                      password="vagrant",
                                      protocol="ssh")
    # create CRUD service
    crud = CRUDService()

    ospf = xr_ipv4_ospf_cfg.Ospf()  # create object
    config_ospf(ospf)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, ospf)

    exit()
    # End of script
