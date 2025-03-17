# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import sys
import time

from src.constants.config import RED, GREEN, BLUE, GRAY, PRCategory, OPENEULER, SRC_OPENEULER
from src.show.base_show import BaseShow
from src.utils.read_conf_yaml import conf
from src.utils.common import write_to_stream
from src.utils.exception import BaseCustomException


class PullRequests(BaseShow):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.category = kwargs.get('category')
        self.repo_name = kwargs.get('repo_name')
        self.oe = kwargs.get('oe')
        self.state = kwargs.get('state')

    def run(self):
        user_info = self._get_user_info()
        user_login = user_info['login']
        if self.repo_name:
            data = self._get_repo_pr(self.repo_name, user=user_login)
        else:
            data = self._get_all_pr()
        data = sorted(data, key=lambda x: int(time.mktime(time.strptime(x['created_at'][:-6], '%Y-%m-%dT%H:%M:%S'))), reverse=True)
        self._show_pr(data)

    def _get_user_repos(self):
        data = []
        current_page = 1
        while True:
            address = self.api_url + conf.get('api', 'user_repos') + \
            f'?access_token={self._decode_auth()}&page={current_page}&per_page={self.per_page}'
            page = self._requests_data(address)
            data += page
            if len(page) < self.per_page:
                break
            current_page += 1
        return data

    def _get_my_create_project(self):
        user_repos = self._get_user_repos()
        user_info = self._get_user_info()
        user_create_repos = []
        for repo in user_repos:
            if repo['full_name'].startswith(user_info['login']):
                user_create_repos.append(repo)
        return user_create_repos

    def _get_all_pr(self):
        user_info = self._get_user_info()
        user_login = user_info['login']
        user_repos = self._get_my_create_project()
        data = []
        full_names = []
        for repo in user_repos:
            full_name = repo['full_name']
            if full_name not in full_names:
                data += self._get_and_filter_oe_pr(repo, user_login)
                full_names.append(full_name)
            if not repo['fork'] or not repo['parent']:
                continue
            parent_full_name = repo['parent']['full_name']
            if parent_full_name not in full_names:
                full_names.append(parent_full_name)
                data += self._get_and_filter_oe_pr(repo['parent'], user_login)
        return data

    def _get_and_filter_oe_pr(self, repo, user_login):
        data = []
        full_name = repo['full_name']
        namespace = repo.get('namespace', {}).get('path', '')
        if self.oe and namespace not in [OPENEULER, SRC_OPENEULER]:
            return data
        data += self._get_repo_pr(full_name, user=user_login)
        return data

    def _filter_oe_enterprise_pr(self, data):
        if not self.oe:
            return data
        result = []
        for item in data:
            pr_namespace = item.get('base', {}).get('repo', {}).get('namespace', {}).get('path', '')
            if pr_namespace in [OPENEULER, SRC_OPENEULER]:
                result.append(item)
        return result

    def _get_repo_pr(self, repo_name, user):
        data = []
        current_page = 1
        while True:
            url = self.api_url + conf.get('api', 'repos_pulls').format(repo_name) + \
                    f'?access_token={self._decode_auth()}&page={current_page}&per_page={self.per_page}' \
                    f'&state={self.state}'
            if self.category == PRCategory.AUTHOR:
                url += f'&author={user}'
            if self.category == PRCategory.ASSIGNEE:
                url += f'&assignee={user}'
            if self.category == PRCategory.TESTER:
                url += f'&tester={user}'
            try:
                page = self._requests_data(url)
            except BaseCustomException as exp:
                write_to_stream(exp.message + '\n', stream=sys.stderr)
                break
            data += page
            if len(page) < self.per_page:
                break
            current_page += 1
        return self._filter_oe_enterprise_pr(data)

    def _show_pr(self, data):
        if self.json:
            self._json_print(data)
            return
        title = ['state', 'mergeable', 'title', 'url', 'head', 'base']
        data_info = []
        for pr in data:
            if pr['state'] == 'open':
                info = [GREEN, f"[{pr['state']}]"]
            elif pr['state'] == 'closed':
                info = [RED, f"[{pr['state']}]"]
            elif pr['state'] == 'merged':
                info = [BLUE, f"[{pr['state']}]"]
            else:
                info = [GRAY, f"[{pr['state']}]"]
            if pr['head']['repo']:
                head_full_name = pr['head']['repo']['full_name']
            else:
                head_full_name = 'Has been deleted'
            if pr['base']['repo']:
                base_full_name = pr['base']['repo']['full_name']
            else:
                base_full_name = 'Has been deleted'
            info += [
                    str(pr['mergeable']), pr['title'], pr['html_url'],
                    f"{head_full_name}:{pr['head']['label']}",
                    f"{base_full_name}:{pr['base']['label']}"
                ]
            data_info.append(info)
        if self.pretty:
            self._pretty_print(data_info, title)
        else:
            self._simple_print(data_info, title)
