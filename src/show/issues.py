# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from src.constants.config import RED, GREEN, YELLOW, BLUE, GRAY
from src.show.base_show import BaseShow
from src.utils.read_conf_yaml import conf


class Issues(BaseShow):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.create = kwargs.get('create')
        self.sort = kwargs.get('sort')
        self.direction = kwargs.get('direction')

    def run(self):
        data = self._get_issues()
        self._show_issues(data)

    def _get_issues(self):
        data = []
        current_page = 1
        if self.create:
            filter = 'created'
        else:
            filter = 'assigned'
        while True:
            page = self._requests_data(self.api_url + conf.get('api', 'user_issues') + \
                    f'?access_token={self._decode_auth()}&page={current_page}&per_page={self.per_page}&filter={filter}'
                    f'&state=all&sort={self.sort}&direction={self.direction}')
            data += page
            if len(page) < self.per_page:
                break
            current_page += 1
        return data

    def _show_issues(self, data):
        if self.json:
            self._json_print(data)
            return
        title = ['state', 'number', 'title', 'login', 'url']
        data_info = []
        for issue in data:
            if issue['state'] == 'open':
                color = GREEN
            elif issue['state'] == 'closed':
                color = RED
            elif issue['state'] == 'processing':
                color = BLUE
            elif issue['state'] == 'rejected':
                color = YELLOW
            else:
                color = GRAY
            info = [color, f"[{issue['state']}]", issue['number'], issue['title'], issue['user']['login'],
                    issue['html_url']]
            data_info.append(info)
        if self.pretty:
            self._pretty_print(data_info, title)
        else:
            self._simple_print(data_info, title)
