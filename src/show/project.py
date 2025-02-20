# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from src.constants.config import RED, GREEN
from src.show.base_show import BaseShow
from src.utils.read_conf_yaml import conf


class Project(BaseShow):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.create = kwargs.get('create')
        self.sort = kwargs.get('sort')
        self.direction = kwargs.get('direction')

    def run(self):
        data = self._get_my_project()
        self._show_project(data)

    def _get_user_repos(self):
        data = []
        current_page = 1
        while True:
            address = self.api_url + conf.get('api', 'user_repos') + \
            f'?access_token={self._decode_auth()}&page={current_page}&per_page={self.per_page}&sort={self.sort}'
            if self.direction:
                address += f'&{self.direction}'
            page = self._requests_data(address)
            data += page
            if len(page) < self.per_page:
                break
            current_page += 1
        return data

    def _get_my_project(self):
        user_repos = self._get_user_repos()
        if not self.create:
            return user_repos
        user_info = self._get_user_info()
        user_create_repos = []
        for repo in user_repos:
            if repo['full_name'].startswith(user_info['login']):
                user_create_repos.append(repo)
        return user_create_repos

    def _show_project(self, data):
        if self.json:
            self._json_print(data)
            return
        title = ['state', 'human_name', 'full_name', 'url']
        data_info = []
        for repo in data:
            info = []
            if repo['public']:
                info = [GREEN, '[public]']
            else:
                info = [RED, '[private]']
            info += [repo['human_name'], repo['full_name'], repo['html_url']]
            data_info.append(info)
        if self.pretty:
            self._pretty_print(data_info, title)
        else:
            self._simple_print(data_info, title)
