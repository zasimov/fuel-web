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

import traceback
from flask import request

from nailgun.database import db
from nailgun.api.models import Node
from nailgun.api.validators.node import NodeVolumesValidator
from nailgun.volumes.manager import VolumeManager
from nailgun.volumes.manager import DisksFormatConvertor
from nailgun.api.models import Node, NodeAttributes
from nailgun.api.handlers.base import JSONHandler, content_json
from nailgun.errors import errors
from nailgun.logger import logger


class NodeDisksHandler(JSONHandler):

    validator = NodeVolumesValidator

    @content_json
    def get(self, node_id):
        node = self.get_object_or_404(Node, node_id)
        node_volumes = node.attributes.volumes
        return DisksFormatConvertor.format_disks_to_simple(node_volumes)

    @content_json
    def put(self, node_id):
        node = self.get_object_or_404(Node, node_id)
        data = self.checked_data()
        if node.cluster:
            node.cluster.add_pending_changes('disks', node_id=node.id)

        volumes_data = DisksFormatConvertor.format_disks_to_full(node, data)
        # For some reasons if we update node attributes like
        #   node.attributes.volumes = volumes_data
        # after
        #   db().commit()
        # it resets to previous state
        db.session.query(NodeAttributes).filter_by(
            node_id=node_id
        ).update({'volumes': volumes_data})
        db.session.commit()

        return DisksFormatConvertor.format_disks_to_simple(
            node.attributes.volumes)


class NodeDefaultsDisksHandler(JSONHandler):

    @content_json
    def get(self, node_id):
        node = self.get_object_or_404(Node, node_id)
        if not node.attributes:
            self.abort(404)

        volumes = DisksFormatConvertor.format_disks_to_simple(
            node.volume_manager.gen_volumes_info())

        return volumes


class NodeVolumesInformationHandler(JSONHandler):

    @content_json
    def get(self, node_id):
        node = self.get_object_or_404(Node, node_id)

        volumes_info = []
        try:
            volumes_info = DisksFormatConvertor.get_volumes_info(node)
        except errors.CannotFindVolumesInfoForRole as exc:
            logger.error(traceback.format_exc())
            self.abort(
                404,
                'Cannot calculate volumes info. '
                'Please, add node to a cluster.'
            )

        return volumes_info
