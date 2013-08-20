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

from nailgun.db import db
from nailgun.errors import errors
from nailgun.api.models import Cluster, Release
from nailgun.api.validators.base import BasicValidator


class ClusterValidator(BasicValidator):

    @classmethod
    def _validate_common(cls, data):
        d = cls.validate_json(data)
        if d.get("release"):
            release = db().query(Release).get(d.get("release"))
            if not release:
                raise errors.InvalidData(
                    "Invalid release id",
                    log_message=True
                )
        if d.get("extended_attrs"):
            ExtendedAttributesValidator.validate(
                d.get("extended_attrs")
            )
        return d

    @classmethod
    def validate(cls, data):
        d = cls._validate_common(data)
        if d.get("name"):
            if db().query(Cluster).filter_by(
                name=d["name"]
            ).first():
                raise errors.AlreadyExists(
                    "Environment with this name already exists",
                    log_message=True
                )
        return d

    @classmethod
    def validate_update(cls, data):
        return cls._validate_common(data)


class AttributesValidator(BasicValidator):
    @classmethod
    def validate(cls, data):
        d = cls.validate_json(data)
        if "generated" in d:
            raise errors.InvalidData(
                "It is not allowed to update generated attributes",
                log_message=True
            )
        if "editable" in d and not isinstance(d["editable"], dict):
            raise errors.InvalidData(
                "Editable attributes should be a dictionary",
                log_message=True
            )
        return d

    @classmethod
    def validate_fixture(cls, data):
        """
        Here we just want to be sure that data is logically valid.
        We try to generate "generated" parameters. If there will not
        be any error during generating then we assume data is
        logically valid.
        """
        d = cls.validate_json(data)
        if "generated" in d:
            cls.traverse(d["generated"])


class ExtendedAttributesValidator(BasicValidator):
    @classmethod
    def validate(cls, data):
        if not isinstance(data, dict):
            raise errors.InvalidData(
                "Extended attributes should be a dictionary",
                log_message=True
            )

        subset = set(data.keys()) <= set(('nodes', 'attributes'))
        if not subset:
            raise errors.InvalidData(
                "Extended attributes include bad attrs: {0}".format(
                    ", ".join(bad_attrs)
                ),
                log_message=True
            )

        if data.get("nodes"):
            if not isinstance(data.get("nodes"), list):
                raise errors.InvalidData(
                    "Extended attributes include "
                    "incorrect list of nodes",
                    log_message=True
                )
            for node in data.get("nodes"):
                if "id" not in node:
                    raise errors.InvalidData(
                        "Extended attributes include "
                        "nodes without ID specified",
                        log_message=True
                    )
