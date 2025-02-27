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

import yaml

from src.constants.config import CONF_YAML, DOT_OEGITEXT
from src.utils.exception import BaseCustomException


class ReadConfYaml:
    def __init__(self, config_path):
        self.config_path = config_path
        self.conf = {}
        self.__init_conf()

    def __init_conf(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding="utf-8") as f:
                self.conf = yaml.load(f.read(), Loader=yaml.FullLoader)

    def get(self, primary_parameter, secondary_parameter=None, tertiary_parameter=None):
        result = ""
        try:
            result = self.conf[primary_parameter]
            if secondary_parameter:
                result = result[secondary_parameter]
            if tertiary_parameter:
                result = result[tertiary_parameter]
        except Exception as e:
            raise BaseCustomException(f'read config failed: {e}')
        return result

    def write_yaml(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, encoding='utf-8', mode='w') as f:
            yaml.dump(self.conf, stream=f, allow_unicode=True, sort_keys=False)


def get_conf():
    src_conf = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', CONF_YAML))
    if os.path.exists(src_conf):
        conf_yaml = ReadConfYaml(src_conf)
    else:
        raise BaseCustomException(f'read config failed, config file {src_conf} not exists')
    return conf_yaml


def get_user_conf():
    current_user_home = os.path.expanduser("~")
    user_conf_path = os.path.join(current_user_home, DOT_OEGITEXT, CONF_YAML)
    conf_yaml = ReadConfYaml(user_conf_path)
    return conf_yaml


conf = get_conf()
user_conf = get_user_conf()
