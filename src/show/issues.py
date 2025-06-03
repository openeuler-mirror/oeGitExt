# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from src.constants.config import RED, GREEN, YELLOW, BLUE, GRAY, OPENEULER, SRC_OPENEULER, IssueFilter
from src.show.base_show import BaseShow
from src.utils.read_conf_yaml import conf


class Issues(BaseShow):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.filter = kwargs.get('filter')
        self.sort = kwargs.get('sort')
        self.direction = kwargs.get('direction')
        self.oe = kwargs.get('oe')
        self.state = kwargs.get('state')

    def run(self):
        data = self._get_issues()
        self._show_issues(data)

    def _filter_oe_enterprise_issue(self, data, login):
        if not self.oe:
            return data
        result = []
        for item in data:
            if self.filter == IssueFilter.ALL:
                user_login = item.get('user', {}).get('login', {})
                assigned = item.get('assignee', {})
                assigned_login = ''
                if assigned:
                    assigned_login = assigned.get('login', {})
                if login not in [user_login, assigned_login]:
                    continue
            enterprise = item.get('repository', {}).get('enterprise', {})
            if not enterprise:
                continue
            issue_namespace = enterprise.get('name', '').lower()
            if issue_namespace in [OPENEULER, SRC_OPENEULER]:
                result.append(item)
        return result

    def _get_issues_by_filter(self, address, filter):
        data = []
        current_page = 1
        while True:
            page = self._requests_data(address + f'&filter={filter}')
            data += page
            if len(page) < self.per_page:
                break
            current_page += 1
        return data

    def _get_issues(self):
        data = []
        current_page = 1
        user_info = self._get_user_info()
        address = self.api_url + conf.get('api', 'user_issues') + \
                    f'?access_token={self._decode_auth()}&page={current_page}&per_page={self.per_page}' \
                    f'&state={self.state}&sort={self.sort}&direction={self.direction}'
        if self.filter in [IssueFilter.ALL, IssueFilter.ASSIGNED]:
            data += self._get_issues_by_filter(address, IssueFilter.ASSIGNED)
        if self.filter in [IssueFilter.ALL, IssueFilter.CREATED]:
            data += self._get_issues_by_filter(address, IssueFilter.CREATED)
        return self._filter_oe_enterprise_issue(data, user_info['login'])

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
