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

import os
import sys
import argparse
import code
import web
import logging


def syncdb_action(params):
    """
    sync application database
    """
    from nailgun.logger import logger
    from nailgun.db import syncdb
    logger.info("Syncing database...")
    syncdb()
    logger.info("Done")

def dropdb_action(params):
    """
    drop application database
    """
    from nailgun.logger import logger
    from nailgun.db import dropdb
    logger.info("Dropping database...")
    dropdb()
    logger.info("Done")

def test_action(params):
    """
    run unit tests
    """
    from nailgun.logger import logger
    from nailgun.unit_test import TestRunner
    logger.info("Running tests...")
    TestRunner.run()
    logger.info("Done")

def loaddata_action(params):
    """
    load data from fixture
    """
    from nailgun.logger import logger
    from nailgun.fixtures import fixman
    logger.info("Uploading fixture...")
    with open(params.fixture, "r") as fileobj:
        fixman.upload_fixture(fileobj)
    logger.info("Done")

def dumpdata_action(params):
    """
    dump data to JSON
    """
    logging.disable(logging.WARNING)
    from nailgun.fixtures import fixman
    fixman.dump_fixture(params.model)

def loaddefault_action(params):
    """
    load data from default fixtures
    (settings.FIXTURES_TO_IPLOAD)
    """
    from nailgun.logger import logger
    from nailgun.fixtures import fixman
    logger.info("Uploading fixture...")
    fixman.upload_fixtures()
    logger.info("Done")

def run_action(params):
    """
    run application locally
    """
    from nailgun.settings import settings
    from nailgun.wsgi import appstart
    settings.update({
        'LISTEN_PORT': int(params.port),
        'LISTEN_ADDRESS': params.address,
    })
    for attr in ['FAKE_TASKS', 'FAKE_TASKS_TICK_COUNT',
                 'FAKE_TASKS_TICK_INTERVAL', 'FAKE_TASKS_AMQP']:
        param = getattr(params, attr.lower())
        if param is not None:
            settings.update({attr: param})
    if params.config_file:
        settings.update_from_file(params.config_file)
    appstart(keepalive=params.keepalive)

def shell_action(params):
    """
    open python REPL
    """
    from nailgun.settings import settings
    if params.config_file:
        settings.update_from_file(params.config_file)
    try:
        from IPython import embed
        embed()
    except ImportError:
        code.interact(local={'db': db, 'settings': settings})

def dump_settings_action(params):
    """
    dump current settings to YAML
    """
    from nailgun.settings import settings
    sys.stdout.write(settings.dump())


if __name__ == "__main__":
    actions = {
        "run": {
            "action": run_action,
            "args": [
                {
                    "args": ["-p", "--port"],
                    "params": {
                        "dest": "port",
                        "action": "store",
                        "type": str,
                        "help": "application port",
                        "default": "8000"
                    }
                },
                {
                    "args": ["-a", "--address"],
                    "params": {
                        "dest": "address",
                        "action": "store",
                        "type": str,
                        "help": "application address",
                        "default": "0.0.0.0"
                    }
                },
                {
                    "args": ["-c", "--config"],
                    "params": {
                        "dest": "config_file",
                        "action": "store",
                        "type": str,
                        "help": "custom config file",
                        "default": None
                    }
                },
                {
                    "args": ["--fake-tasks"],
                    "params": {
                        "action": "store_true",
                        "help": "fake tasks"
                    }
                },
                {
                    "args": ["--fake-tasks-tick-count"],
                    "params": {
                        "action": "store",
                        "type": int,
                        "help": "Fake tasks tick count"
                    }
                },
                {
                    "args": ["--fake-tasks-tick-interval"],
                    "params": {
                        "action": "store",
                        "type": int,
                        "help": "Fake tasks tick interval"
                    }
                },
                {
                    "args": ["--fake-tasks-amqp"],
                    "params": {
                        "action": "store_true",
                        "help": "fake tasks with real amqp"
                    }
                },
                {
                    "args": ["--keepalive"],
                    "params": {
                        "action": "store_true",
                        "help": "run keepalive thread"
                    }
                },

            ]
        },
        "test": {
            "action": test_action
        },
        "syncdb": {
            "action": syncdb_action
        },
        "dropdb": {
            "action": dropdb_action
        },
        "shell": {
            "action": shell_action,
            "args": [
                {
                    "args": ["-c", "--config"],
                    "params": {
                        "dest": "config_file",
                        "action": "store",
                        "type": str,
                        "help": "custom config file",
                        "default": None
                    }
                },
            ]
        },
        "loaddata": {
            "action": loaddata_action,
            "args": [
                {
                    "args": ["fixture"],
                    "params": {
                        "action": "store",
                        "help": "json fixture to load"
                    }
                },
            ]
        },
        "dumpdata": {
            "action": dumpdata_action,
            "args": [
                {
                    "args": ["model"],
                    "params": {
                        "action": "store",
                        "help": "model name to dump; "
                                "underscored name "
                                "should be used, e.g. "
                                "network_group for "
                                "for NetworkGroup model"
                    }
                },
            ]
        },
        "loaddefault": {
            "action": loaddefault_action
        },
        "dump_settings": {
            "action": dump_settings_action
        }
    }
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
