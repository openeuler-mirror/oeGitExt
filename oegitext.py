#!/usr/bin/python3
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

from src.command_line.parsers.client_parser import ClientParser
from src.utils.common import write_to_stream
from src.utils.exception import BaseCustomException


if __name__ == '__main__':
    try:
        ClientParser().execute()
    except BaseCustomException as ex:
        write_to_stream(str(ex) + '\n', stream=sys.stderr)
        sys.exit(1)
