# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from src.constants.config import RED, GREEN, BLUE, GRAY
from src.show.base_show import BaseShow
from src.utils.read_conf_yaml import conf


class PullRequests(BaseShow):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.only_mine = kwargs.get('only_mine')
        self.repo_name = kwargs.get('repo_name')

    def run(self):
        data = self._get_repo_pr()
        self._show_pr(data)

    def _get_repo_pr(self):
        data = []
        current_page = 1
        while True:
            page = self._requests_data(self.api_url + conf.get('api', 'repos_pulls').format(self.repo_name) + \
                    f'?access_token={self._decode_auth()}&page={current_page}&per_page={self.per_page}&state=all')
            data += page
            if len(page) < self.per_page:
                break
            current_page += 1
        if not self.only_mine:
            return data
        user_info = self._get_user_info()
        user_login = user_info['login']
        mine_pr = []
        for pr in data:
            if pr['user']['login'] == user_login:
                mine_pr.append(pr)
        return mine_pr

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
            info += [
                    str(pr['mergeable']), pr['title'], pr['html_url'],
                    f"{pr['head']['repo']['full_name']}:{pr['head']['label']}",
                    f"{pr['base']['repo']['full_name']}:{pr['base']['label']}"
                ]
            data_info.append(info)
        if self.pretty:
            self._pretty_print(data_info, title)
        else:
            self._simple_print(data_info, title)
