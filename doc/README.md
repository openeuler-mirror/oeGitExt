# oeGitExt

## 1. 配置gitee私人令牌

```
oegitext config -token ${access_token}
```

## 2. Show project
```
oegitext show proj [-h] [-create] [-p] [-j] [-s {full_name,created,updated,pushd}] [-d {,desc,asc}] [-c COLUMNS]
参数说明：
  -h, --help        显示帮助信息
  -create           仅显示我创建的工程
  -p, --pretty      以pretty格式显示结果
  -j, --json        以json格式显示结果
  -s, --sort        排序依据: 创建时间(created)，更新时间(updated)
  -d, --direction   排序方式，升序或者降序
  -c， --columns    仅显示指定列
```
### 显示我的项目
```
oegitext show proj
# 以pretty格式显示
oegitext show proj -p
oegitext show proj --pretty
# 仅显示项目的state和url列
oegitext show proj -c state,url
oegitext show proj --columns state,url
# 以pretty格式显示
oegitext show proj -c state,url -p
oegitext show proj --columns state,url --pretty
```

### 显示我创建的项目
```
oegitext show proj -create
# 以pretty格式显示
oegitext show proj -create -p
oegitext show proj -create --pretty
# 仅显示项目的state和url列
oegitext show proj -create -c state,url
oegitext show proj -create --columns state,url
# 以pretty格式显示
oegitext show proj -create -c state,url -p
oegitext show proj -create --columns state,url --pretty
```

## 3. Show issues
```
oegitext show issue [-h] [-oe] [-create] [-p] [-j] [-s {created,updated}] [-d {desc,asc}] [-c COLUMNS]
                    [-state {all,open,closed,progressing,rejected}]
参数说明：
  -h, --help        显示帮助信息
  -oe               仅显示openEuler企业仓issue
  -create           仅显示我创建的issue
  -p, --pretty      以pretty格式显示结果
  -j, --json        以json格式显示结果
  -s, --sort        排序依据: 创建时间(created)，更新时间(updated)
  -d, --direction   排序方式，升序或者降序
  -c, --columns     仅显示指定列
  -stage            根据状态过滤issue，all,open,closed,progressing,rejected，默认为open
```
### 显示我负责的issues
```
oegitext show issue
# 以pretty格式显示
oegitext show issue -p
oegitext show issue --pretty
# 仅显示state和url列
oegitext show issue -c state,url
oegitext show issue --columns state,url
# 以pretty格式显示
oegitext show issue -c state,url -p
oegitext show issue --columns state,url --pretty
```

### 显示我创建的issues
```
oegitext show issue -create
# 以pretty格式显示
oegitext show issue -create -p
oegitext show issue -create --pretty
# 仅显示state和url列
oegitext show issue -create -c state,url
oegitext show issue -create --columns state,url
# 以pretty格式显示
oegitext show issue -create -c state,url -p
oegitext show issue -create --columns state,url --pretty
```

## 4. Show pull request
```
oegitext show pr [-h] [-oe] [-name REPO_NAME] [-category {all,author,assignee,tester}] 
                 [-state {all,open,closed,merged}] [-p] [-j] [-c COLUMNS]
参数说明：
  -h, --help        显示帮助信息
  -oe               仅显示openEuler企业仓issue
  -name             pr所属name，未指定显示用户所有pr
  -category         根据用户角色过滤PR，all,open,closed,merged，默认为all
  -stage            根据状态过滤PR，all,author,assignee,tester，默认为open
  -p, --pretty      以pretty格式显示结果
  -j, --json        以json格式显示结果
  -c, --columns     仅显示指定列
```
### 显示仓库的PR
```
oegitext show pr -name src-openeuler/vscode
# 以pretty格式显示
oegitext show pr -name src-openeuler/vscode -p
oegitext show pr -name src-openeuler/vscode --pretty
# 仅显示其中的state和url列
oegitext show pr -name src-openeuler/vscode -c state,url
oegitext show pr -name src-openeuler/vscode --columns state,url
# 以pretty格式显示
oegitext show pr -name src-openeuler/vscode -c state,url -p
oegitext show pr -name src-openeuler/vscode --columns state,url --pretty
```

### 仅显示仓库中我创建的PR
```
oegitext show pr -name src-openeuler/vscode -category create
```

### 显示我创建的所有PR
```
oegitext show pr -category author
```
### 显示我审查的所有PR
```
oegitext show pr -category assignee
```
### 显示我测试的所有PR
```
oegitext show pr -category tester
```

## 5. Show repos
```
oegitext show repo [-h] [-owner {openeuler,src-openeuler}] [-p] [-j] [-c COLUMNS]
参数说明：
  -h, --help        显示帮助信息
  -owner            仓库所有者openeuler,src-openeuler，默认openeuler
  -p, --pretty      以pretty格式显示结果
  -j, --json        以json格式显示结果
  -c, --columns     仅显示指定列

```

### 显示openeuler的repos
```
oegitext show repo
oegitext show repo -owner openeuler
# 以pretty格式显示
oegitext show repo -owner openeuler -p
oegitext show repo -owner openeuler --pretty
# 仅显示其中的state和url列
oegitext show repo -owner openeuler -c state,url
oegitext show repo -owner openeuler --columns state,url
# 以pretty格式显示
oegitext show repo -owner openeuler -c state,url -p
oegitext show repo -owner openeuler --columns state,url --pretty
```

### 显示src-openeuler的repos
```
oegitext show repo -owner src-openeuler
# 以pretty格式显示
oegitext show repo -owner src-openeuler -p
oegitext show repo -owner src-openeuler --pretty
# 仅显示其中的state和url列
oegitext show repo -owner src-openeuler -c state,url
oegitext show repo -owner src-openeuler --columns state,url
# 以pretty格式显示
oegitext show repo -owner src-openeuler -c state,url -p
oegitext show repo -owner src-openeuler --columns state,url --pretty
```

## 6. fork

```
oegitext fork [-h] -user USER -repo REPO [-org ORG] [-name NAME] [-path PATH] [-show]
参数说明：
  -h, --help  显示帮助信息
  -user USER  仓库所属空间地址(企业、组织或个人的地址path)
  -repo REPO  仓库路径(path)
  -org  ORG   组织空间完整地址，不填写默认Fork到用户个人空间地址
  -name NAME  fork 后仓库名称。默认: 源仓库名称
  -path PATH  fork 后仓库地址。默认: 源仓库地址
  -show       显示requests结果
```
## 7. 处理issue

```
oegitext issue [-h] -cmd {create,update,close,open,get} [-user USER] [-repo REPO] [-title TITLE] [-number NUMBER] 
               [-body BODY] [-show]
参数说明：
  -h, --help      显示帮助信息
  -cmd            处理issue命令
  -user USER      issue所属空间地址(企业、组织或个人的地址path)
  -repo REPO      仓库路径(path)
  -title TITLE    title
  -number NUMBER  issue number
  -body BODY      issue body
  -show           显示requests结果
```

### 获取仓库issue
```
issue -cmd get -user USER -repo REPO -number NUMBER [-show]
```
### 创建issue
```
issue -cmd create -user USER -repo REPO -title TITLE [-body BODY] [-show]
```
### 更新issue
```
issue -cmd update -user USER -repo REPO -title TITLE -number NUMBER [-body BODY] [-show]
```
### 关闭issue
```
issue -cmd close -user USER -repo REPO -number NUMBER [-show]
```
### 打开issue
```
issue -cmd open -user USER -repo REPO -number NUMBER [-show]
```

## 8. 处理PR
```
oegitext pull [-h] -cmd {create,update,close,open,review,test,merge,get} [-user USER] [-repo REPO] [-title TITLE]
              [-head HEAD] [-base BASE] [-number NUMBER] [-body BODY] [-state STATE] [-show]
参数说明：
  -h, --help      显示帮助信息
  -cmd            处理PR命令, create,update,close,open,review,test,merge,get
  -user USER      PR所属空间地址(企业、组织或个人的地址path)
  -repo REPO      仓库路径(path)
  -title TITLE    title
  -head HEAD      PR提交的源分支。格式：branch (master) 或者：path_with_namespace:branch (oschina/gitee:master)
  -base BASE      RP提交目标分支的名称
  -number NUMBER  number
  -body           RP内容
  -state STATE    state
  -show           显示requests结果

```

### 获取PR
```
oegitext pull -cmd get -user USER -repo REPO -number NUMBER [-show]
```
### 创建PR
```
oegitext pull -cmd create -user USER -repo REPO -title TITLE -head HEAD -base BASE [-body BODY] [-show]
参数说明：
  -head HEAD: Pull Request 提交的源分支。格式：branch (master) 或者：path_with_namespace:branch (oschina/gitee:master)
  -base BASE: Pull Request 提交目标分支的名称
```
### 更新PR
```
oegitext pull -cmd update -user USER -repo REPO -number NUMBER -body BODY [-show]
```
### 关闭PR
```
oegitext pull -cmd close -user USER -repo REPO -number NUMBER [-show]
```
### 打开PR
```
oegitext pull -cmd open -user USER -repo REPO -number NUMBER [-show]
```
### 强制review通过
```
oegitext pull -cmd open -user USER -repo REPO -number NUMBER [-show]
```
### review PR
```
oegitext pull -cmd review -user USER -repo REPO -number NUMBER -state {pass,reset} [-show]
参数说明：
  -state pass:  强制review通过
         reset: 重置review状态
```
### test PR
```
oegitext pull -cmd test -user USER -repo REPO -number NUMBER -state {pass,reset} [-show]
参数说明：
  -state pass:  强制测试通过
         reset: 重置测试状态
```
### merge PR
```
oegitext pull -cmd merge -user USER -repo REPO -number NUMBER [-show]
```
