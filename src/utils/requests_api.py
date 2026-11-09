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
import time
import requests

from requests.exceptions import RequestException

from src.utils.exception import BaseCustomException
from src.utils.read_conf_yaml import conf, user_conf

# 网络异常后的重试间隔（秒）。未写入 yaml，避免旧配置缺少该键时读取即失败
RETRY_INTERVAL = 1


class RequestsApi:
    def __init__(self):
        self.headers = conf.get('headers')
        self.times = conf.get('requests', 'retry_times')
        self.timeout = conf.get('requests', 'timeout')
        self.api_type = user_conf.get('api_type')

    def _mask_token(self, text):
        """抹掉文本中的 access_token，避免凭据出现在报错信息里。"""
        if self.api_type == 'gitee':
            return re.sub('access_token=[a-f0-9]{32}', 'access_token=***', text)
        return re.sub('access_token=[a-zA-Z0-9\-]{24}', 'access_token=***', text)

    def requests_get(self, address):
        result = []
        network_error = None
        for attempt in range(self.times):
            network_error = None
            try:
                response = requests.get(address, headers=self.headers, timeout=self.timeout)
            except RequestException as e:
                # 连接失败、读超时等网络异常归入重试，不让 retry_times 形同虚设
                network_error = e
                if attempt + 1 < self.times:
                    time.sleep(RETRY_INTERVAL)
                continue
            if response.status_code >= 200 and response.status_code <= 206:
                content = response.content.decode(encoding='UTF-8')
                result = json.loads(content)
                break
        else:
            add_url = self._mask_token(address)
            if network_error is not None:
                error = self._mask_token(str(network_error))
                raise BaseCustomException(
                    f'request {add_url} failed: {type(network_error).__name__}: {error}')
            raise BaseCustomException(f'request {add_url} failed: status code: {response.status_code}: reason: {response.reason}')
        return result

    def requests_post(self, address, data=None):
        result = ''
        if not isinstance(data, str):
            data = json.dumps(data)
        network_error = None
        for attempt in range(self.times):
            network_error = None
            try:
                response = requests.post(address, data=data, headers=self.headers, timeout=self.timeout)
            except RequestException as e:
                # 写操作重试存在重复提交风险，但远胜于旧版本的直接抛异常 + 不重试
                network_error = e
                if attempt + 1 < self.times:
                    time.sleep(RETRY_INTERVAL)
                continue
            if response.status_code >= 200 and response.status_code <= 206:
                result = response.content.decode(encoding='UTF-8')
                break
        else:
            add_url = self._mask_token(address)
            if network_error is not None:
                error = self._mask_token(str(network_error))
                raise BaseCustomException(
                    f'post {add_url} failed: {type(network_error).__name__}: {error}')
            raise BaseCustomException(f'post {add_url} failed: status code: {response.status_code}: reason: {response.reason}: text: {response.text}')
        return result

    def requests_patch(self, address, data=None):
        if not isinstance(data, str):
            data = json.dumps(data)
        result = ''
        network_error = None
        for attempt in range(self.times):
            network_error = None
            try:
                response = requests.patch(address, data=data, headers=self.headers, timeout=self.timeout)
            except RequestException as e:
                network_error = e
                if attempt + 1 < self.times:
                    time.sleep(RETRY_INTERVAL)
                continue
            if response.status_code >= 200 and response.status_code <= 206:
                result = response.content.decode(encoding='UTF-8')
                break
        else:
            add_url = self._mask_token(address)
            if network_error is not None:
                error = self._mask_token(str(network_error))
                raise BaseCustomException(
                    f'patch {add_url} failed: {type(network_error).__name__}: {error}')
            raise BaseCustomException(f'patch {add_url} failed: status code: {response.status_code}: reason: {response.reason}: text: {response.text}')
        return result

    def requests_put(self, address, data=None):
        if not isinstance(data, str):
            data = json.dumps(data)
        result = ''
        network_error = None
        for attempt in range(self.times):
            network_error = None
            try:
                response = requests.put(address, data=data, headers=self.headers, timeout=self.timeout)
            except RequestException as e:
                network_error = e
                if attempt + 1 < self.times:
                    time.sleep(RETRY_INTERVAL)
                continue
            if response.status_code >= 200 and response.status_code <= 206:
                result = response.content.decode(encoding='UTF-8')
                break
        else:
            add_url = self._mask_token(address)
            if network_error is not None:
                error = self._mask_token(str(network_error))
                raise BaseCustomException(
                    f'put {add_url} failed: {type(network_error).__name__}: {error}')
            raise BaseCustomException(f'put {add_url} failed: status code: {response.status_code}: reason: {response.reason}: text: {response.text}')
        return result


requests_api = RequestsApi()
