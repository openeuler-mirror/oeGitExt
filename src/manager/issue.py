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

from src.manager.mamager_base import ManagerBase
from src.utils.common import decode_auth
from src.utils.exception import BaseCustomException
from src.utils.read_conf_yaml import conf
from src.utils.requests_api import requests_api


class Issue(ManagerBase):
    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def run(self):
        cmd_str = f'_{self.kwargs["cmd"]}_issue'
        if hasattr(self, cmd_str):
            result = getattr(self, cmd_str)()
            self._show_result(result)
        else:
            raise BaseCustomException(f'bad issue command: {self.kwargs["cmd"]}')

    def _create_issue(self):
        data = {
            'access_token': decode_auth(self.auth),
            'repo': self.kwargs['repo'],
            'title': self.kwargs['title']
        }
        if self.kwargs['body']:
            data['body'] = self.kwargs['body']
        address = self.api_url + conf.get('api', 'repos_user_issues').format(self.kwargs["user"])
        return requests_api.requests_post(address, data)

    def _close_issue(self):
        data = {
            'access_token': decode_auth(self.auth),
            'repo': self.kwargs['repo'],
            'title': self.kwargs['title'],
            'state': "closed"
        }
        if self.kwargs['body']:
            data['body'] = self.kwargs['body']
        address = self.api_url + conf.get('api', 'user_issues_number').format(self.kwargs["user"],
                                            self.kwargs["number"])
        return requests_api.requests_patch(address, data)

    def _open_issue(self):
        data = {
            'access_token': decode_auth(self.auth),
            'repo': self.kwargs['repo'],
            'title': self.kwargs['title'],
            'state': "open"
        }
        if self.kwargs['body']:
            data['body'] = self.kwargs['body']
        address = self.api_url + conf.get('api', 'user_issues_number').format(self.kwargs["user"], self.kwargs["number"])
        return requests_api.requests_patch(address, data)

    def _update_issue(self):
        data = {
            'access_token': decode_auth(self.auth),
            'repo': self.kwargs['repo'],
            'title': self.kwargs['title']
        }
        if self.kwargs['body']:
            data['body'] = self.kwargs['body']
        address = self.api_url + conf.get('api', 'user_issues_number').format(self.kwargs["user"], self.kwargs["number"])
        return requests_api.requests_patch(address, data)

    def _get_issue(self):
        address = self.api_url + conf.get('api', 'user_repo_issues_number').format(self.kwargs["user"], self.kwargs['repo'], self.kwargs["number"]) + f'?access_token={decode_auth(self.auth)}'
        result = requests_api.requests_get(address)
        return json.dumps(result)
