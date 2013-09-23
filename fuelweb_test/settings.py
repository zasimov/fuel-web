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


import os

ISO_PATH = os.environ.get('ISO_PATH')
EMPTY_SNAPSHOT = os.environ.get('EMPTY_SNAPSHOT', 'empty')
OPENSTACK_RELEASE = os.environ.get('OPENSTACK_RELEASE', 'Grizzly')

REDHAT_USERNAME = os.environ.get('REDHAT_USERNAME')
REDHAT_PASSWORD = os.environ.get('REDHAT_PASSWORD')
REDHAT_SATELLITE_HOST = os.environ.get('REDHAT_SATELLITE_HOST')
REDHAT_ACTIVATION_KEY = os.environ.get('REDHAT_ACTIVATION_KEY')

INTERFACE_ORDER = ('internal', 'public', 'private', 'nat')

PUBLIC_FORWARD = os.environ.get('PUBLIC_FORWARD', None)

FORWARDING = {
    'public': PUBLIC_FORWARD,
    'internal': None,
    'private': None,
    'nat': 'nat',
}

DHCP = {
    'public': False,
    'internal': False,
    'private': False,
    'nat': True,
}

INTERFACES = {
    'internal': 'eth0',
    'public': 'eth1',
    'private': 'eth2',
    'nat': 'eth3',
}

DEFAULT_POOLS = {
    'public': '10.108.0.0/16:24',
    'private': '10.108.0.0/16:24',
    'internal': '10.108.0.0/16:24',
    'nat': '10.108.0.0/16:24',
}

POOLS = {
    'public': os.environ.get('PUBLIC_POOL',
                             DEFAULT_POOLS.get('public')).split(':'),
    'private': os.environ.get('PRIVATE_POOL',
                              DEFAULT_POOLS.get('private')).split(':'),
    'internal': os.environ.get('INTERNAL_POOL',
                               DEFAULT_POOLS.get('internal')).split(':'),
    'nat': os.environ.get('NAT_POOL',
                          DEFAULT_POOLS.get('nat')).split(':'),
}

NETWORK_TYPES = {
    #todo: !!!values are undefined currently, need  to be specified!!!
    #todo: refactor when the real values will be availalbe
    'nova': 'novanetwork',
    'neutron'   : 'ovs'
}

NEUTRON_SEGMENTATION_TYPES = {
    #todo: values from doc https://docs.google.com/a/mirantis.com/document/d/1-GCoxHeHrm-E329DgK8U2n4EYN9uW2q8RjnwCf2Zb90/edit?usp=sharing
    #todo: refactor when the real values will be availalbe
    'vlan'  : 'gre',
    'gre'   : {'name' : 'gre',
               'enable_tunneling': 'true',
               'tunnel_range': '1:65534',
               'tunnel_bridge' : 'br_tun',
               'local_ip' : '10.108.0.254'
    }, #gre
    'lisp'  : 'lisp',
    'vxlan' : 'vxlan'
}

NETWORK_MANAGERS = {
    'flat': 'FlatDHCPManager',
    'vlan': 'VlanManager'
}

CLEAN = os.environ.get('CLEAN', 'true') == 'true'
LOGS_DIR = os.environ.get('LOGS_DIR')
