# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import json
import re

from src.constants.config import RESET, MAGENTA
from src.utils.common import write_to_stream, decode_auth
from src.utils.exception import BaseCustomException
from src.utils.read_conf_yaml import conf, user_conf
from src.utils.requests_api import requests_api


class BaseShow:
    def __init__(self, kwargs):
        self.pretty = kwargs.get('pretty')
        self.json = kwargs.get('json')
        self.api_url = conf.get('api_url')
        self.gitee_url = conf.get('gitee_url')
        self.headers = conf.get('headers')
        self.times = conf.get('requests', 'retry_times')
        self.per_page = conf.get('requests', 'per_page')
        self.auth = user_conf.get('token')
        self.columns = []
        self.__init_columns(kwargs.get('columns'))

    def __init_columns(self, columns):
        for item in columns.split(','):
            item = item.strip()
            if not item or item in self.columns:
                continue
            self.columns.append(item)

    @staticmethod
    def _count_str_len(data):
        str_len = 0
        if not data:
            return str_len
        for item in data:
            if re.match(r'[\u4e00-\u9fa5]', item):
                str_len += 2
            else:
                str_len += 1
        return str_len

    def _decode_auth(self):
        return decode_auth(self.auth)

    def _requests_data(self, address):
        return requests_api.requests_get(address)

    def _pretty_print(self, data, title):
        width = [0] * len(title)
        item_width = [[self._count_str_len(item) for item in row[1:]] for row in data]
        item_width.append([len(item) for item in title])
        for row in item_width:
            for index in range(len(width)):
                if row[index] > width[index] - 1:
                    width[index] = row[index] + 1
        width[-1] -= 1
        data_info = []
        title_info = []
        for col, word_width in zip(title, width):
            title_info.append(col + ' ' * (word_width - len(col)))
        data_info.append(title_info)
        for row in data:
            item_str_info = [f'{row[0]}{row[1]}' + ' ' * (width[0] - self._count_str_len(row[1])) + RESET]
            for item, word_width in zip(row[2:], width[1:]):
                if item is None:
                    item = ''
                item_str_info.append(item + ' ' * (word_width - self._count_str_len(item)))
            data_info.append(item_str_info)

        if not self.columns:
            self._pretty_print_data(data_info)
            return
        if not (set(self.columns) & set(title)):
            raise BaseCustomException(f'columns "{",".join(self.columns)}" not exists')
        print_data_info = []
        for row in data_info:
            new_row = []
            for index, item in enumerate(title):
                if item in self.columns:
                    new_row.append(row[index])
            print_data_info.append(new_row)
        self._pretty_print_data(print_data_info)

    def _pretty_print_data(self, data_info):
        command_str = []
        command_str.append(MAGENTA + ''.join(data_info[0]) + RESET)
        for row in data_info[1:]:
            command_str.append(''.join(row).strip())
        write_to_stream('\n'.join(command_str) + '\n')

    def _simple_print(self, data, title):
        print_data_info = [row[1:] for row in data]
        if self.columns:
            if not (set(self.columns) & set(title)):
                raise BaseCustomException(f'columns "{",".join(self.columns)}" not exists')
            print_data_info = []
            for row in data:
                new_row = []
                for index, item in enumerate(title):
                    if item in self.columns:
                        new_row.append(row[index + 1])
                print_data_info.append(new_row)
        command_str = []
        for row in print_data_info:
            for index in range(len(row)):
                if row[index] is None:
                    row[index] = ''
            command_str.append(': '.join(row).strip())
        write_to_stream('\n'.join(command_str) + '\n')

    def _json_print(self, data):
        if self.pretty:
            data_str = json.dumps(data, indent=2) + '\n'
        else:
            data_str = json.dumps(data)
        write_to_stream(data_str)

    def _get_user_info(self):
        data = self._requests_data(self.api_url + conf.get('api', 'user') + f'?access_token={self._decode_auth()}')
        return data
