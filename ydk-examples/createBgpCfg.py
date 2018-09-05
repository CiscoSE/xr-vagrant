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
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_cfg \
    as xr_ipv4_bgp_cfg
from ydk.models.cisco_ios_xr import Cisco_IOS_XR_ipv4_bgp_datatypes \
    as xr_ipv4_bgp_datatypes
from ydk.types import Empty



def config_bgp(bgp):
    """Add config data to bgp object."""
    # global configuration
    instance = bgp.Instance()
    instance.instance_name = "default"
    instance_as = instance.InstanceAs()
    instance_as.as_ = 0
    four_byte_as = instance_as.FourByteAs()
    four_byte_as.as_ = 65001
    four_byte_as.bgp_running = Empty()
    # global address family
    global_af = four_byte_as.default_vrf.global_.global_afs.GlobalAf()
    global_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamily.ipv4_unicast
    global_af.enable = Empty()
    four_byte_as.default_vrf.global_.global_afs.global_af.append(global_af)
    instance_as.four_byte_as.append(four_byte_as)
    instance.instance_as.append(instance_as)
    bgp.instance.append(instance)

    # configure IBGP neighbor group
    neighbor_groups = four_byte_as.default_vrf.bgp_entity.neighbor_groups
    neighbor_group = neighbor_groups.NeighborGroup()
    neighbor_group.neighbor_group_name = "IBGP"
    neighbor_group.create = Empty()
    # remote AS
    neighbor_group.remote_as.as_xx = 0
    neighbor_group.remote_as.as_yy = 65001
    neighbor_group.update_source_interface = "Loopback0"
    neighbor_groups.neighbor_group.append(neighbor_group)
    # ipv4 unicast
    neighbor_group_af = neighbor_group.neighbor_group_afs.NeighborGroupAf()
    neighbor_group_af.af_name = xr_ipv4_bgp_datatypes.BgpAddressFamily.ipv4_unicast
    neighbor_group_af.activate = Empty()
    neighbor_group_afs = neighbor_group.neighbor_group_afs
    neighbor_group_afs.neighbor_group_af.append(neighbor_group_af)

    # configure IBGP neighbor
    neighbor = four_byte_as.default_vrf.bgp_entity.neighbors.Neighbor()
    neighbor.neighbor_address = "172.16.255.2"
    neighbor.neighbor_group_add_member = "IBGP"
    four_byte_as.default_vrf.bgp_entity.neighbors.neighbor.append(neighbor)


if __name__ == "__main__":
    """Execute main program."""

    # create NETCONF provider
    provider = NetconfServiceProvider(address="localhost",
                                      port=57779,
                                      username="vagrant",
                                      password="vagrant",
                                      protocol="ssh")
    # create CRUD service
    crud = CRUDService()

    bgp = xr_ipv4_bgp_cfg.Bgp()  # create object
    config_bgp(bgp)  # add object configuration

    # create configuration on NETCONF device
    crud.create(provider, bgp)

    exit()
# End of script