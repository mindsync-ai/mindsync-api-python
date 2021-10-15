#!/usr/bin/env python
#
# Copyright 2021 Mindsync
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# coding=utf-8

from setuptools import setup, find_packages

setup(
    name='mindsync',
    version='0.0.1',
    description='Mindsync API',
    long_description=
    ('Official API for https://api.mindsync.ai, accessible using a command line '
     'tool implemented in Python.'),
    author='Mindsync',
    author_email='support@mindsync.ai',
    url='https://github.com/mindsync-ai/mindsync-api-python',
    keywords=['Mindsync', 'API'],
    entry_points={'console_scripts': ['mindsync = mindsync:main']},
    install_requires=[
        'aiohttp==3.7.4.post0',
        'pytest-asyncio==0.15.1'
    ],
    packages=find_packages(),
    license='Apache 2.0')
