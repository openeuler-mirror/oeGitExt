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

from src.constants.config import RESET, PullsCommand
from src.manager.mamager_base import ManagerBase
from src.utils.common import decode_auth
from src.utils.exception import BaseCustomException
from src.utils.read_conf_yaml import conf
from src.utils.requests_api import requests_api


class Pull(ManagerBase):
    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def run(self):
        cmd_str = f'_{self.kwargs["cmd"]}_pull_request'
        if hasattr(self, cmd_str):
            result = getattr(self, cmd_str)()
            self._show_result(result)
        else:
            raise BaseCustomException(f'bad issue command: {self.kwargs["cmd"]}')

    def _create_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls').format(self.kwargs["user"], self.kwargs["repo"])
        data = {
            'access_token': decode_auth(self.auth),
            "title": self.kwargs['title'],
            "head": self.kwargs['head'],
            "base": self.kwargs['base']
        }
        if self.kwargs['body']:
            data['body'] = self.kwargs['body']
        return requests_api.requests_post(address, data)

    def _close_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_number').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"])
        data = {
            'access_token': decode_auth(self.auth),
            'state': 'closed'
        }
        return requests_api.requests_patch(address, data)

    def _open_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_number').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"])
        data = {
            'access_token': decode_auth(self.auth),
            'state': 'open'
        }
        return requests_api.requests_patch(address, data)

    def _update_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_number').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"])
        data = {
            'access_token': decode_auth(self.auth),
            "body": self.kwargs['body']
        }
        return requests_api.requests_patch(address, data)

    def _review_pass_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_review').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"])
        data = {
            'access_token': decode_auth(self.auth),
            "force": "true"
        }
        return requests_api.requests_post(address, data)

    def _review_reset_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_assignees').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"])
        data = {
            'access_token': decode_auth(self.auth),
            "reset_all": "true"
        }
        return requests_api.requests_patch(address, data)

    def _test_pass_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_test').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"])
        data = {
            'access_token': decode_auth(self.auth),
            "force": "true"
        }
        return requests_api.requests_post(address, data)

    def _test_reset_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_testers').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"])
        data = {
            'access_token': decode_auth(self.auth),
            "reset_all": "true"
        }
        return requests_api.requests_patch(address, data)

    def _merge_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_merge').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"])
        data = {
            'access_token': decode_auth(self.auth),
            "merge_method": "merge"
        }
        return requests_api.requests_put(address, data)

    def _get_pull_requests(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_number').format(self.kwargs["user"],
                    self.kwargs["repo"], self.kwargs["number"]) + f'?access_token={decode_auth}'
        return requests_api.requests_get(address)
    
    def _review_pull_request(self):
        if self.kwargs['state'] == PullsCommand.PASS:
            return self._review_pass_pull_request()
        if self.kwargs['state'] == PullsCommand.RESET:
            return self._review_reset_pull_request()
        raise BaseCustomException(f'bad review state: {self.kwargs["state"]}')

    def _test_pull_request(self):
        if self.kwargs['state'] == PullsCommand.PASS:
            return self._test_pass_pull_request()
        if self.kwargs['state'] == PullsCommand.RESET:
            return self._test_reset_pull_request()
        raise BaseCustomException(f'bad test state: {self.kwargs["state"]}')

    def _get_pull_request(self):
        address = self.api_url + conf.get('api', 'user_repo_pulls_number').format(self.kwargs["user"],
                    self.kwargs['repo'], self.kwargs["number"]) + f'?access_token={decode_auth(self.auth)}'
        result = requests_api.requests_get(address)
        return json.dumps(result)
