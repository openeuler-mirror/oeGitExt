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

from src.command_line.parsers.common_parser import common_parser
from src.utils.exception import BaseCustomException


class BaseParser:
    def __init__(self):
        self.command_name = ""
        self.main_description = ""
        self.main_parser = None

    def execute(self):
        try:
            args = self.main_parser.parse_args()
        except IndexError as err:
            self.main_parser.print_help()
            raise BaseCustomException('Parameter parsing error') from err

        if not hasattr(args, 'func'):
            self.main_parser.print_help()
            raise BaseCustomException('Parameter parsing error')
        args.func(args)

    def _get_main_parser(self):
        main_parser = argparse.ArgumentParser(
            prog=self.command_name,
            description=self.main_description,
            parents=[common_parser.parser],
        )
        return main_parser

    def _get_action(self):
        action = self.main_parser.add_subparsers(title='subcommands')
        return action
