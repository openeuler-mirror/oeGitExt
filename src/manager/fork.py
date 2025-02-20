# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from src.manager.mamager_base import ManagerBase
from src.utils.common import decode_auth
from src.utils.read_conf_yaml import conf
from src.utils.requests_api import requests_api


class Fork(ManagerBase):
    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def run(self):
        result = self._fork()
        self._show_result(result)

    def _fork(self):
        address = self.api_url + conf.get('api', 'user_repo_forks').format(self.kwargs["user"], self.kwargs["repo"])
        data = {
            'access_token': decode_auth(self.auth),
        }
        if self.kwargs['name']:
            data['name'] = self.kwargs['name']
        if self.kwargs['path']:
            data['path'] = self.kwargs['path']
        if self.kwargs['org']:
            data['organization'] = self.kwargs['org']
        return requests_api.requests_post(address, data)
