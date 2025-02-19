# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import json
import re
import requests

from src.utils.exception import BaseCustomException
from src.utils.read_conf_yaml import conf


class RequestsApi:
    def __init__(self):
        self.headers = conf.get('headers')
        self.times = conf.get('requests', 'retry_times')
        self.timeout = conf.get('requests', 'timeout')

    def requests_get(self, address):
        result = []
        for _ in range(self.times):
            response = requests.get(address, headers=self.headers, timeout=self.timeout)
            if response.status_code >= 200 and response.status_code <= 206:
                content = response.content.decode(encoding='UTF-8')
                result = json.loads(content)
                break
        else:
            add_url = re.sub('access_token=[a-f0-9]{32}', 'access_token=***', address)
            raise BaseCustomException(f'request {add_url} failed: status code: {response.status_code}: reason: {response.reason}')
        return result

    def requests_post(self, address, data=None):
        result = ''
        if not isinstance(data, str):
            data = json.dumps(data)
        for _ in range(self.times):
            response = requests.post(address, data=data, headers=self.headers, timeout=self.timeout)
            if response.status_code >= 200 and response.status_code <= 206:
                result = response.content.decode(encoding='UTF-8')
                break
        else:
            add_url = re.sub('access_token=[a-f0-9]{32}', 'access_token=***', address)
            raise BaseCustomException(f'post {add_url} failed: status code: {response.status_code}: reason: {response.reason}: text: {response.text}')
        return result

    def requests_patch(self, address, data=None):
        if not isinstance(data, str):
            data = json.dumps(data)
        result = ''
        for _ in range(self.times):
            response = requests.patch(address, data=data, headers=self.headers, timeout=self.timeout)
            if response.status_code >= 200 and response.status_code <= 206:
                result = response.content.decode(encoding='UTF-8')
                break
        else:
            add_url = re.sub('access_token=[a-f0-9]{32}', 'access_token=***', address)
            raise BaseCustomException(f'patch {add_url} failed: status code: {response.status_code}: reason: {response.reason}: text: {response.text}')
        return result

    def requests_put(self, address, data=None):
        if not isinstance(data, str):
            data = json.dumps(data)
        result = ''
        for _ in range(self.times):
            response = requests.put(address, data=data, headers=self.headers, timeout=self.timeout)
            if response.status_code >= 200 and response.status_code <= 206:
                result = response.content.decode(encoding='UTF-8')
                break
        else:
            add_url = re.sub('access_token=[a-f0-9]{32}', 'access_token=***', address)
            raise BaseCustomException(f'put {add_url} failed: status code: {response.status_code}: reason: {response.reason}: text: {response.text}')
        return result


requests_api = RequestsApi()
