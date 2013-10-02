# -*- coding: utf-8 -*-

#    Copyright 2013 Mirantis, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from nailgun.api.models import NeutronConfig
from nailgun.db import db


class NeutronManager(object):

    def create_neutron_config(self, cluster):
        meta = cluster.release.networks_metadata["neutron"]["config"]
        neutron_config = NeutronConfig(
            cluster_id=cluster.id,
            parameters=meta["parameters"],
            predefined_networks=self._generate_predefined_networks(),
            l2=self._generate_l2(),
            l3=self._generate_l3(),
            segmentation_type=cluster.net_segment_type
        )
        db().add(neutron_config)
        db().flush()

    def _generate_predefined_networks(self):
        return {
            "net04_ext": {
                "shared": False,
                "L2": {
                    "router_ext": True,
                    "network_type": "flat",
                    "physnet": "physnet1"
                },
                "L3": {
                    "subnet": "10.100.100.0/24",
                    "gateway": None,
                    "nameservers": [],
                    "public": True,
                    "floating": "10.100.100.130:10.100.100.254"
                }
            },
            "net04": {
                "L2": {
                    "router_ext": False,
                    "network_type": "gre",
                    "physnet": "physnet2"
                },
                "L3": {
                    "subnet": "192.168.111.0/24",
                    "gateway": None,
                    "nameservers": ["8.8.4.4", "8.8.8.8"],
                    "public": False,
                    "floating": None
                }
            }
        }

    def _generate_l2(self):
        return {
            "base_mac": "fa:16:3e:00:00:00",
            "segmentation_type": "vlan",
            "tunnel_id_ranges": "1:65534",
            "bridge_mappings": [
                "physnet1:br-ex",
                "physnet2:br-prv"
            ],
            "network_vlan_ranges": [
                "physnet1",
                "physnet2:1000:2999"
            ],
            "phys_nets": {
                "physnet1": {
                    "bridge": "br-ex",
                    "vlan_range": ""
                },
                "physnet2": {
                    "bridge": "br-prv",
                    "vlan_range": ""
                }
            }
        }

    def _generate_l3(self):
        return {}

    def get_predefined_networks(self, cluster):
        return cluster.neutron_config.predefined_networks
