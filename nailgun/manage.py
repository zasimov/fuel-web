#!/usr/bin/env python
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

import sys
import argparse

from nailgun.actions import actions

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(
        dest="action", help='actions'
    )

    for action, params in actions.iteritems():
        action_parser = subparsers.add_parser(
            action, help=params["action"].__doc__
        )
        for arg in params.get("args", []):
            action_parser.add_argument(
                *arg["args"],
                **arg["params"]
            )

    params, other_params = parser.parse_known_args()
    sys.argv.pop(1)

    if not params.action in actions:
        parser.print_help()
        sys.exit(0)

    actions[params.action]["action"](params)
