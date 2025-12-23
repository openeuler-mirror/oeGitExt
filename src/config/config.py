# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import base64
import os
import re

from src.utils.exception import BaseCustomException
from src.utils.read_conf_yaml import user_conf


class Config:
    def __init__(self, token, api_type):
        self.token = token
        self.api_type = api_type

    def run(self):
        if self.api_type == 'gitee' and not re.match("^[a-f0-9]{32}$", self.token):
            raise BaseCustomException("bad token format")
        user_conf.conf['token'] = base64.b64encode(self.token.encode()).decode()
        user_conf.conf['api_type'] = self.api_type
        user_conf.write_yaml()
