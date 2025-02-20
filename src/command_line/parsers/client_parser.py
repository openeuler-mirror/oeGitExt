# -*- coding: utf-8 -*-

# Copyright: Copyright (c) 2024 Huawei Technologies Co., Ltd.
# oeGitExt is licensed under the Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#     http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

from src.command_line.parsers.base_parser import BaseParser
from src.config.config import Config
from src.constants.config import OPENEULER, SRC_OPENEULER, Sort, IssuesCommand, PullsCommand
from src.show.issues import Issues
from src.show.project import Project
from src.show.pull_requests import PullRequests
from src.show.repos import Repos
from src.manager.fork import Fork
from src.manager.issue import Issue
from src.manager.pull import Pull


class ClientParser(BaseParser):
    def __init__(self):
        super().__init__()
        self.command_name = "oegitext"
        self.main_description = \
            "oegitext is used to help developers seamlessly leverage the openEuler community infrastructure"
        self.main_parser = self._get_main_parser()
        self.action = self._get_action()
        self._add_config_parser()
        self.show_action = self._add_show_parser()
        self._add_show_project_parser()
        self._add_show_issues_parser()
        self._add_show_pull_request_parser()
        self._add_show_repos_parser()
        self._add_forks_parser()
        self._add_issues_parser()
        self._add_pulls_parser()

    @staticmethod
    def _run_config_access_token(args):
        Config(args.token).run()

    @staticmethod
    def _run_show_project(args):
        Project(create=args.create, pretty=args.pretty, columns=args.columns, json=args.json, sort=args.sort,
                direction=args.direction).run()

    @staticmethod
    def _run_show_issues(args):
        Issues(create=args.create, pretty=args.pretty, columns=args.columns, json=args.json, sort=args.sort,
                direction=args.direction).run()

    @staticmethod
    def _run_show_pull_request(args):
        PullRequests(repo_name=args.repo_name, only_mine=args.only, pretty=args.pretty, columns=args.columns,
                    json=args.json).run()

    @staticmethod
    def _run_show_repos(args):
        Repos(owner=args.owner, pretty=args.pretty, columns=args.columns, json=args.json).run()

    @staticmethod
    def _run_fork(args):
        Fork(user=args.user, repo=args.repo, org=args.org, name=args.name, path=args.path, show=args.show).run()

    @staticmethod
    def _run_issue(args):
        Issue(cmd=args.cmd, user=args.user, repo=args.repo, title=args.title, number=args.number, body=args.body,
            show=args.show).run()

    @staticmethod
    def _run_pull(args):
        Pull(cmd=args.cmd, user=args.user, repo=args.repo, title=args.title, head=args.head, base=args.base,
            number=args.number, state=args.state, body=args.body, show=args.show).run()

    def _add_show_parser(self):
        show_parser = self.action.add_parser(
            'show',
            help='show repos info'
        )
        show_action = show_parser.add_subparsers(
            title="show", 
            description="show repos info"
        )
        return show_action

    def _add_config_parser(self):
        config_parser = self.action.add_parser(
            'config',
            help='config gitee access token'
        )
        config_parser.add_argument(
            '-token',
            required=True,
            help='access token'
        )
        config_parser.set_defaults(func=self._run_config_access_token)

    def _add_show_project_parser(self):
        project_parser = self.show_action.add_parser(
            'proj',
            help='show project'
        )
        project_parser.add_argument(
            '-create',
            action='store_true',
            default=False,
            help='only show my create project'
        )
        project_parser.add_argument(
            '-p', '--pretty',
            dest='pretty',
            action='store_true',
            default=False,
            help='show in pretty format'
        )
        project_parser.add_argument(
            '-j', '--json',
            dest='json',
            action='store_true',
            default=False,
            help='show in json format'
        )
        project_parser.add_argument(
            '-s', '--sort',
            dest='sort',
            default=Sort.FULL_NAME,
            choices=[Sort.FULL_NAME, Sort.CREATED, Sort.UPDATED, Sort.PUSHD],
            help='sort rules'
        )
        project_parser.add_argument(
            '-d', '--direction',
            dest='direction',
            default='',
            choices=['', Sort.DESC, Sort.ASC],
            help='sort rules'
        )
        project_parser.add_argument(
            '-c', '--columns',
            dest='columns',
            default='',
            help='only show specific columns'
        )
        project_parser.set_defaults(func=self._run_show_project)

    def _add_show_issues_parser(self):
        issues_parser = self.show_action.add_parser(
            'issue',
            help='show issues'
        )
        issues_parser.add_argument(
            '-create',
            action='store_true',
            default=False,
            help='only show my create issues'
        )
        issues_parser.add_argument(
            '-p', '--pretty',
            dest='pretty',
            action='store_true',
            default=False,
            help='show in pretty format'
        )
        issues_parser.add_argument(
            '-j', '--json',
            dest='json',
            action='store_true',
            default=False,
            help='show in json format'
        )
        issues_parser.add_argument(
            '-s', '--sort',
            dest='sort',
            default=Sort.CREATED,
            choices=[Sort.CREATED, Sort.UPDATED],
            help='sort rules'
        )
        issues_parser.add_argument(
            '-d', '--direction',
            dest='direction',
            default=Sort.DESC,
            choices=[Sort.DESC, Sort.ASC],
            help='sort rules'
        )
        issues_parser.add_argument(
            '-c', '--columns',
            dest='columns',
            default='',
            help='only show specific columns'
        )
        issues_parser.set_defaults(func=self._run_show_issues)

    def _add_show_pull_request_parser(self):
        pull_request_parser = self.show_action.add_parser(
            'pr',
            help='show pull request'
        )
        pull_request_parser.add_argument(
            '-name',
            dest="repo_name",
            required=True,
            help='repo name'
        )
        pull_request_parser.add_argument(
            '-only',
            action='store_true',
            default=False,
            help='only show my own'
        )
        pull_request_parser.add_argument(
            '-p', '--pretty',
            dest='pretty',
            action='store_true',
            default=False,
            help='show in pretty format'
        )
        pull_request_parser.add_argument(
            '-j', '--json',
            dest='json',
            action='store_true',
            default=False,
            help='show in json format'
        )
        pull_request_parser.add_argument(
            '-c', '--columns',
            dest='columns',
            default='',
            help='only show specific columns'
        )
        pull_request_parser.set_defaults(func=self._run_show_pull_request)

    def _add_show_repos_parser(self):
        repo_parser = self.show_action.add_parser(
            'repo',
            help='show repos'
        )
        repo_parser.add_argument(
            '-owner',
            default=OPENEULER,
            choices=[OPENEULER, SRC_OPENEULER],
            help='repo owner'
        )
        repo_parser.add_argument(
            '-p', '--pretty',
            dest='pretty',
            action='store_true',
            default=False,
            help='show in pretty format'
        )
        repo_parser.add_argument(
            '-j', '--json',
            dest='json',
            action='store_true',
            default=False,
            help='show in json format'
        )
        repo_parser.add_argument(
            '-c', '--columns',
            dest='columns',
            default='',
            help='only show specific columns'
        )
        repo_parser.set_defaults(func=self._run_show_repos)

    def _add_forks_parser(self):
        forks_parser = self.action.add_parser(
            'fork',
            help='fork repos'
        )
        forks_parser.add_argument(
            '-user',
            required=True,
            help='source repo user name'
        )
        forks_parser.add_argument(
            '-repo',
            required=True,
            help='source repo name'
        )
        forks_parser.add_argument(
            '-org',
            help='organization path'
        )
        forks_parser.add_argument(
            '-name',
            help='repo name after fork'
        )
        forks_parser.add_argument(
            '-path',
            help='repo path after fork'
        )
        forks_parser.add_argument(
            '-show',
            action='store_true',
            default=False,
            help='show request results'
        )
        forks_parser.set_defaults(func=self._run_fork)

    def _add_issues_parser(self):
        issues_parser = self.action.add_parser(
            'issue',
            help='manage issues'
        )
        issues_parser.add_argument(
            '-cmd',
            required=True,
            choices=[
                IssuesCommand.CREATE, IssuesCommand.UPDATE, IssuesCommand.CLOSE, IssuesCommand.OPEN,
                IssuesCommand.GET
                    ],
            help='issue command'
        )
        issues_parser.add_argument(
            '-user',
            help='source repo user name'
        )
        issues_parser.add_argument(
            '-repo',
            help='source repo name'
        )
        issues_parser.add_argument(
            '-title',
            help='issue title'
        )
        issues_parser.add_argument(
            '-number',
            help='issue number, no need to add #'
        )
        issues_parser.add_argument(
            '-body',
            help='issue body'
        )
        issues_parser.add_argument(
            '-show',
            action='store_true',
            default=False,
            help='show request results'
        )
        issues_parser.set_defaults(func=self._run_issue)

    def _add_pulls_parser(self):
        pulls_parser = self.action.add_parser(
            'pull',
            help='manage pull requests'
        )
        pulls_parser.add_argument(
            '-cmd',
            required=True,
            choices=[
                PullsCommand.CREATE, PullsCommand.UPDATE, PullsCommand.CLOSE, PullsCommand.OPEN,
                PullsCommand.REVIEW, PullsCommand.TEST, PullsCommand.MERGE, PullsCommand.GET
                ],
            help='PR command'
        )
        pulls_parser.add_argument(
            '-user',
            help='source repo user name'
        )
        pulls_parser.add_argument(
            '-repo',
            help='source repo name'
        )
        pulls_parser.add_argument(
            '-title',
            help='issue title'
        )
        pulls_parser.add_argument(
            '-head',
            help='PR source branch name'
        )
        pulls_parser.add_argument(
            '-base',
            help='PR target branch name'
        )
        pulls_parser.add_argument(
            '-number',
            help='PR number'
        )
        pulls_parser.add_argument(
            '-body',
            help='PR body'
        )
        pulls_parser.add_argument(
            '-state',
            help='state'
        )
        pulls_parser.add_argument(
            '-show',
            action='store_true',
            default=False,
            help='show request results'
        )
        pulls_parser.set_defaults(func=self._run_pull)
