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


import logging
import unittest
from devops.helpers.helpers import wait
from nose.plugins.attrib import attr
from fuelweb_test.helpers import Ebtables
from fuelweb_test.integration.base_node_test_case import BaseNodeTestCase
from fuelweb_test.integration.decorators import snapshot_errors, \
    debug, fetch_logs
from fuelweb_test.settings import EMPTY_SNAPSHOT

logging.basicConfig(
    format=':%(lineno)d: %(asctime)s %(message)s',
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)
logwrap = debug(logger)


class TestNode(BaseNodeTestCase):
    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_neutron_node_provisioning(self):
        self.prepare_environment()
        cluster_id = self.create_cluster(name="neutron")
        self._basic_provisioning(
            cluster_id=cluster_id,
            nodes_dict={'slave-01': ['neutron']}
            #todo: check this when this role will be available really
                    )
        #todo: check real state when neutron will be available
        self.run_OSTF(cluster_id=cluster_id, should_fail=22, should_pass=0)

    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_simple_neutron_cluster(self):
        self.prepare_environment()
        nodes = {'slave-01': ['controller'],
                 'slave-02': ['compute'],
                 'slave_03': ['cinder'],
                 'slave_04': ['neutron']}
        cluster_id = self.create_cluster(name='neutron')
        #todo: check this when the API for the client will be ready
        self.update_vlan_network_fixed(cluster_id, amount=5, network_size=32)
        self._basic_provisioning(cluster_id, nodes)
        self.assertClusterReady(
            'slave-01', smiles_count=6, networks_count=5, timeout=300)
        self.get_ebtables(cluster_id, self.nodes().slaves[:2]).restore_vlans()
        task = self._run_network_verify(cluster_id)
        self.assertTaskSuccess(task, 60 * 2)
        self.run_OSTF(cluster_id=cluster_id, should_fail=0, should_pass=22)

    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_controller_neutron_node(self):
        self.prepare_environment()
        nodes = {'slave-01': ['controller', 'neutron'],
                 'slave-02': ['compute'],
                 'slave_03': ['cinder']}
        cluster_id = self.create_cluster(name='neutron')
        #todo: check this when the API for the client will be ready
        self.update_vlan_network_fixed(cluster_id, amount=5, network_size=32)
        self._basic_provisioning(cluster_id, nodes)
        self.assertClusterReady(
            'slave-01', smiles_count=6, networks_count=5, timeout=300)
        task = self._run_network_verify(cluster_id)
        self.assertTaskSuccess(task, 60 * 2)
        self.run_OSTF(cluster_id=cluster_id, should_fail=0, should_pass=22)

    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_compute_neutron_node(self):
        self.prepare_environment()
        nodes = {'slave-01': ['controller'],
                 'slave-02': ['compute', 'neutron'],
                 'slave_03': ['cinder']}
        cluster_id = self.create_cluster(name='neutron')
        #todo: check this when the API for the client will be ready
        self.update_vlan_network_fixed(cluster_id, amount=5, network_size=32)
        self._basic_provisioning(cluster_id, nodes)
        self.assertClusterReady(
            'slave-01', smiles_count=6, networks_count=5, timeout=300)
        task = self._run_network_verify(cluster_id)
        self.assertTaskSuccess(task, 60 * 2)
        self.run_OSTF(cluster_id=cluster_id, should_fail=0, should_pass=22)

    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_cinder_neutron_node(self):
        self.prepare_environment()
        nodes = {'slave-01': ['controller'],
                 'slave-02': ['compute'],
                 'slave_03': ['cinder', 'neutron']}
        cluster_id = self.create_cluster(name='neutron')
        #todo: check this when the API for the client will be ready
        self.update_vlan_network_fixed(cluster_id, amount=5, network_size=32)
        self._basic_provisioning(cluster_id, nodes)
        self.assertClusterReady(
            'slave-01', smiles_count=6, networks_count=5, timeout=300)
        task = self._run_network_verify(cluster_id)
        self.assertTaskSuccess(task, 60 * 2)
        self.run_OSTF(cluster_id=cluster_id, should_fail=0, should_pass=22)

    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_controller_neutron_node(self):
        self.prepare_environment()
        nodes = {'slave-01': ['neutron', 'controller'],
                 'slave-02': ['compute'],
                 'slave_03': ['cinder']}
        cluster_id = self.create_cluster(name='neutron')
        #todo: check this when the API for the client will be ready
        self.update_vlan_network_fixed(cluster_id, amount=5, network_size=32)
        self._basic_provisioning(cluster_id, nodes)
        self.assertClusterReady(
            'slave-01', smiles_count=6, networks_count=5, timeout=300)
        task = self._run_network_verify(cluster_id)
        self.assertTaskSuccess(task, 60 * 2)
        self.run_OSTF(cluster_id=cluster_id, should_fail=0, should_pass=22)

    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_neutron_compute_node(self):
        self.prepare_environment()
        nodes = {'slave-01': ['controller'],
                 'slave-02': ['neutron', 'compute'],
                 'slave_03': ['cinder']}
        cluster_id = self.create_cluster(name='neutron')
        #todo: check this when the API for the client will be ready
        self.update_vlan_network_fixed(cluster_id, amount=5, network_size=32)
        self._basic_provisioning(cluster_id, nodes)
        self.assertClusterReady(
            'slave-01', smiles_count=6, networks_count=5, timeout=300)
        task = self._run_network_verify(cluster_id)
        self.assertTaskSuccess(task, 60 * 2)
        self.run_OSTF(cluster_id=cluster_id, should_fail=0, should_pass=22)

    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_neutron_cinder_node(self):
        self.prepare_environment()
        nodes = {'slave-01': ['controller'],
                 'slave-02': ['compute'],
                 'slave_03': ['neutron', 'cinder']}
        cluster_id = self.create_cluster(name='neutron')
        #todo: check this when the API for the client will be ready
        self.update_vlan_network_fixed(cluster_id, amount=5, network_size=32)
        self._basic_provisioning(cluster_id, nodes)
        self.assertClusterReady(
            'slave-01', smiles_count=6, networks_count=5, timeout=300)
        task = self._run_network_verify(cluster_id)
        self.assertTaskSuccess(task, 60 * 2)
        self.run_OSTF(cluster_id=cluster_id, should_fail=0, should_pass=22)

    @snapshot_errors
    @logwrap
    @fetch_logs
    @attr(releases=['centos'])
    def test_double_neutron_cluster(self):
        self.prepare_environment()
        nodes = {'slave-01': ['controller'],
                 'slave-02': ['compute'],
                 'slave_03': ['cinder'],
                 'slave_04': ['neutron', 'neutron']}
        cluster_id = self.create_cluster(name='neutron')
        #todo: check this when the API for the client will be ready
        self.update_vlan_network_fixed(cluster_id, amount=5, network_size=32)
        self._basic_provisioning(cluster_id, nodes)
        # self.assertClusterReady(
        #     'slave-01', smiles_count=6, networks_count=5, timeout=300)
        self.get_ebtables(cluster_id, self.nodes().slaves[:2]).restore_vlans()
        task = self._run_network_verify(cluster_id)
        self.assertTaskFailed(task, 60 * 2)
        self.run_OSTF(cluster_id=cluster_id, should_fail=22, should_pass=0)
