# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import argparse

from src.utils.read_conf_yaml import conf


class CommonParser:
    """
    通用解析器类
    """

    def __init__(self):
        self.parser = self._get_parser()

    @staticmethod
    def _get_parser():
        parser = argparse.ArgumentParser(add_help=False)
        parser.add_argument(
            '-v', '--version', action='version',
            version=conf.get('version'), help='show version'
        )
        return parser


common_parser = CommonParser()
