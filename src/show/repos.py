# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import os

from src.constants.config import GREEN, RED
from src.show.base_show import BaseShow
from src.utils.read_conf_yaml import conf


class Repos(BaseShow):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.owner = kwargs.get('owner')

    def run(self):
        data = self._get_orgs_repos()
        self._show_orgs_repos(data)

    def _get_orgs_repos(self):
        data = []
        current_page = 1
        while True:
            page = self._requests_data(self.api_url + conf.get('api', 'orgs_repos').format(self.owner) + \
                    f'?access_token={self._decode_auth()}&page={current_page}&per_page={self.per_page}')
            data += page
            if len(page) < self.per_page:
                break
            current_page += 1
        return data

    def _show_orgs_repos(self, data):
        if self.json:
            self._json_print(data)
            return
        title = ['state', 'full_name', 'url']
        data_info = []
        for repo in data:
            info = []
            if repo['public']:
                info = [GREEN, '[public]']
            else:
                info = [RED, '[private]']
            info += [repo['full_name'], repo['html_url']]
            data_info.append(info)
        if self.pretty:
            self._pretty_print(data_info, title)
        else:
            self._simple_print(data_info, title)
