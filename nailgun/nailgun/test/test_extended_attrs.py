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

import json

from mock import patch

import nailgun
from nailgun.test.base import BaseHandlers
from nailgun.test.base import fake_tasks
from nailgun.test.base import reverse


class TestExtendedAttrs(BaseHandlers):

    @fake_tasks(fake_rpc=False, mock_rpc=False)
    @patch('nailgun.rpc.cast')
    def test_extended_attrs_merged(self, mocked_rpc):
        self.env.create(
            nodes_kwargs=[
                {"role": "controller", "pending_addition": True}
            ]
        )
        cluster_db = self.env.clusters[0]
        node_db = self.env.nodes[0]
        cluster_db.extended_attrs = {
            "nodes": [
                {"id": node_db.id, "bridges": ["br0", "br1"]}
            ],
            "attributes": {
                "deployment_mode": "ha_full"
            }
        }
        self.db.commit()

        supertask = self.env.launch_deployment()
        args, kwargs = nailgun.task.manager.rpc.cast.call_args

        deployment_task = filter(
            lambda t: t["method"] == "deploy",
            args[1]
        )[0]

        self.assertIn(
            "bridges",
            deployment_task["args"]["nodes"][0]
        )
        self.assertEqual(
            ["br0", "br1"],
            deployment_task["args"]["nodes"][0]["bridges"]
        )
        self.assertEqual(
            "ha_full",
            deployment_task["args"]["attributes"]["deployment_mode"]
        )
