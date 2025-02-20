# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from src.utils.common import write_to_stream
from src.utils.read_conf_yaml import conf, user_conf


class ManagerBase:
    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.api_url = conf.get('api_url')
        self.gitee_url = conf.get('gitee_url')
        self.headers = conf.get('headers')
        self.times = conf.get('requests', 'retry_times')
        self.per_page = conf.get('requests', 'per_page')
        self.auth = user_conf.get('token')
        self.data = None

    def _show_result(self, result):
        if self.kwargs['show']:
            write_to_stream(result + '\n')
