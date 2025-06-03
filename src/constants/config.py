# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

OPENEULER = "openeuler"
SRC_OPENEULER = "src-openeuler"
DOT_OEGITEXT = ".oegitext"
CONF_YAML = "conf.yaml"
OPENEULER_REPOS = "openeuler_repos"

# 颜色设置
RESET = '\033[0m'
RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
GRAY = '\033[0;90m'


class IssueFilter:
    ALL = 'all'
    ASSIGNED = 'assigned'
    CREATED = 'created'


class IssueState:
    ALL = 'all'
    OPEN = 'open'
    PROGRESSING = 'progressing'
    CLOSED = 'closed'
    REJECTED = 'rejected'


class PRState:
    ALL = 'all'
    OPEN = 'open'
    CLOSED = 'closed'
    MERGED = 'merged'


class PRCategory:
    ALL = 'all'
    AUTHOR = 'author'
    ASSIGNEE = 'assignee'
    TESTER = 'tester'


class Sort:
    FULL_NAME = 'full_name'
    CREATED = 'created'
    UPDATED = 'updated'
    PUSHD = 'pushd'
    DESC = 'desc'
    ASC = 'asc'


class IssuesCommand:
    CREATE = 'create'
    UPDATE = 'update'
    CLOSE = 'close'
    OPEN = 'open'
    GET = 'get'


class PullsCommand:
    CREATE = 'create'
    UPDATE = 'update'
    CLOSE = 'close'
    OPEN = 'open'
    REVIEW = 'review'
    TEST = 'test'
    MERGE = 'merge'
    GET = 'get'
    PASS = "pass"
    RESET = "reset"
