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

import time
import functools
import pickle


def memoize(ttl=60):
    """Decorator to cache values from method
    """
    ttl = ttl
    def cacher(func):

        @functools.wraps(func)
        def wrapper(instance, *args, **kwargs):
            now = time.time()
            pickled = pickle.dumps((args, kwargs))
            try:
                value, last_update = instance._cache[pickled]
                if ttl > 0 and now - last_update > ttl:
                    raise AttributeError
            except (KeyError, AttributeError):
                value = func(instance, *args, **kwargs)
                if not hasattr(instance, '_cache'):
                    instance._cache = {}
                instance._cache[pickled] = (value, now)
            return value
        return wrapper
    return cacher
