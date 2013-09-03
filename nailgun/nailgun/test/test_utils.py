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

import unittest
import time
from nailgun.utils import cached_value
from mock import patch


class DummyClass(object):

    @cached_value.memoize(ttl=20)
    def produce(self, some_int):
        return self.multiplier(some_int)

    @cached_value.memoize(ttl=0.01)
    def produce_with_ttl(self, some_int):
        return self.multiplier(some_int)

    def multiplier(self, some_int):
        return some_int**some_int


class TestMemoizeUtil(unittest.TestCase):

    def setUp(self):
        self.dummy = DummyClass()

    def test_memoize_utils(self):
        resp = self.dummy.produce(10)
        self.assertEqual(resp, 10000000000)
        resp = self.dummy.produce(7)
        self.assertEqual(resp, 823543)

    def test_memoize_call_count(self):
        with patch.object(self.dummy, 'multiplier') as multiplier_mock:
            self.dummy.produce(100)
            self.dummy.produce(100)
            multiplier_mock.assert_called_once_with(100)
            self.assertEqual(multiplier_mock.call_count, 1)
            self.dummy.produce(10)
            self.assertEqual(multiplier_mock.call_count, 2)

    def test_memoize_with_ttl(self):
        with patch.object(self.dummy, 'multiplier') as multiplier_mock:
            self.dummy.produce_with_ttl(10)
            time.sleep(0.02)
            self.dummy.produce_with_ttl(10)
            self.assertEqual(multiplier_mock.call_count, 2)
