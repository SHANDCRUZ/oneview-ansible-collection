#!/usr/bin/env python
# -*- coding: utf-8 -*-
###
# Copyright (2016-2017) Hewlett Packard Enterprise Development LP
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import importlib
import pytest
import re
import yaml
import json

from mock import mock
from distutils.version import StrictVersion


class OneViewBaseTest(object):
    EXAMPLES = None

    @pytest.fixture(autouse=True)
    def setUp(self, mock_ansible_module, mock_ov_client, request, testing_module):
        # class_name = type(self).__name__ 
        # ==== TestCertificatesServerModule
        resource_name = type(self).__name__.replace('Test', '').replace('Module', '')
        word1 = re.findall('[A-Z][^A-Z]*', resource_name)
        word1 = str.join('_', word1).lower()
        # if StrictVersion(pytest.__version__) < StrictVersion("3.6"):
        #     marker = request.node.get_marker('resource')
        # else:
        #     marker = request.node.get_closest_marker('resource')
        self.resource = getattr(mock_ov_client, "%s" % (word1))
        self.resource.get_by_name.return_value = self.resource
        self.mock_ov_client = mock_ov_client
        self.mock_ansible_module = mock_ansible_module

    @pytest.fixture
    def testing_module(self):
        resource_name = type(self).__name__.replace('Test', '')
        resource_module_path_name = self.underscore(resource_name.replace('Module', ''))

        testing_module = importlib.import_module('ansible_collections.hpe.oneview.plugins.modules.' + resource_module_path_name)
        self.testing_class = getattr(testing_module, resource_name)
        try:
            # Load scenarios from module examples (Also checks if it is a valid yaml)
            self.EXAMPLES = yaml.load(testing_module.EXAMPLES, yaml.SafeLoader)

        except yaml.scanner.ScannerError:
            message = "Something went wrong while parsing yaml from {}.EXAMPLES".format(self.testing_class.__module__)
            raise Exception(message)
        return testing_module

    def underscore(self, word):
        word = re.findall('[A-Z][^A-Z]*', word)
        word = 'oneview_' + str.join('_', word).lower()
        return word

    def test_main_function_should_call_run_method(self, testing_module, mock_ansible_module):
        mock_ansible_module.params = {'config': 'config.json'}

        main_func = getattr(testing_module, 'main')

        with mock.patch.object(self.testing_class, "run") as mock_run:
            main_func()
            mock_run.assert_called_once()


class OneViewBaseFactsTest(OneViewBaseTest):
    def test_should_get_all_using_filters(self, testing_module):
        self.resource.get_all.return_value = []

        params_get_all_with_filters = dict(
            config='config.json',
            name=None,
            params={
                'start': 1,
                'count': 3,
                'sort': 'name:descending',
                'filter': 'purpose=General',
                'query': 'imported eq true'
            })
        self.mock_ansible_module.params = params_get_all_with_filters

        self.testing_class().run()

        self.resource.get_all.assert_called_once_with(start=1, count=3, sort='name:descending', filter='purpose=General', query='imported eq true')

    def test_should_get_all_without_params(self, testing_module):
        self.resource.get_all.return_value = []

        params_get_all_with_filters = dict(
            config='config.json',
            name=None
        )
        self.mock_ansible_module.params = params_get_all_with_filters

        self.testing_class().run()

        self.resource.get_all.assert_called_once_with()


class ImageStreamerBaseTest(OneViewBaseTest):
    @pytest.fixture
    def mock_ov_client(self, mock_ov_client):
        return mock_ov_client.create_image_streamer_client()

    def underscore(self, word):
        word = re.findall('[A-Z][^A-Z]*', word)
        word = 'image_streamer_' + str.join('_', word).lower()
        return word


class ImageStreamerBaseFactsTest(ImageStreamerBaseTest, OneViewBaseFactsTest):
    pass

class OneViewClientTest(object):
    @classmethod
    def from_json_file(cls, file_name):
        """
        Construct OneViewClient using a json file.

        Args:
            file_name: json full path.

        Returns:
            OneViewClient:
        """
        with open(file_name) as json_data:
            config = json.load(json_data)

        return cls(config)
