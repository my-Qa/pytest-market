# python-api-automation

基于 **pytest + requests + YAML 数据驱动** 的接口自动化测试框架。用例与接口定义分离，支持接口依赖提取、数据库校验、Allure 报告与钉钉机器人通知。

> 项目原为接口自动化练手项目，已完成结构整理与产物治理（运行报告、日志、虚拟环境均不入库）。

## 技术栈

| 组件 | 用途 |
| --- | --- |
| pytest | 用例组织、fixture、钩子扩展 |
| requests | HTTP 接口请求封装 |
| PyYAML / jsonpath | 用例 YAML 数据驱动、响应断言取值 |
| allure-pytest | 测试报告（支持 `--alluredir`） |
| PyMySQL | 数据库查询与数据校验 |
| pandas | CSV 测试数据处理 |
| pytest-ordering | 用例执行顺序控制 |
| PyQt5 | 用例生成/工具界面（`base/new_tools.ui`） |
| 钉钉机器人 | 测试结果推送 |

## 目录结构

```
python_project/
├── base/                     # 底层能力
│   ├── apiutil.py            # 接口调用工具
│   ├── apiutil_business.py   # 业务场景组合封装
│   ├── generateId.py         # 测试数据 ID 生成
│   ├── new_testcase_tools.py # 用例生成工具
│   ├── removefile.py         # 报告临时文件清理
│   └── new_tools.ui          # PyQt5 工具界面
├── common/                   # 公共组件
│   ├── assertions.py         # 断言封装
│   ├── connection.py         # 数据库连接（MySQL）
│   ├── debugtalk.py          # 动态函数库（类似 httprunner）
│   ├── dingRobot.py          # 钉钉机器人推送
│   ├── operationcsv.py       # CSV 读写
│   ├── readyaml.py           # YAML 读写、接口依赖提取
│   ├── recordlog.py          # 日志记录
│   └── sendrequest.py        # 请求发送封装
├── conf/                     # 配置
│   ├── config.ini            # 接口地址 / 数据库配置
│   ├── operationConfig.py    # 配置读取
│   └── setting.py            # 全局开关（报告类型、钉钉推送等）
├── data/                     # 测试数据（账号、车牌号等）
├── testcase/                 # 用例（YAML 定义 + Python 执行）
│   ├── Single interface/     # 单接口用例（增删改查用户）
│   ├── ProductManager/       # 商品模块（商品列表、详情、下单、支付）
│   └── Business interface/   # 业务场景串联用例
├── report/                   # 运行产物（不入库）
├── logs/                     # 运行日志（不入库）
├── conftest.py               # 全局 fixture + 执行统计 + 钉钉推送钩子
├── pytest.ini                # pytest 配置
├── environment.xml           # Allure 环境信息
├── extract.yaml              # 接口依赖提取结果
├── run.py                    # 一键运行入口
└── requirements.txt
```

## 核心设计

**1. YAML 数据驱动**
一条接口用例 = 一段 YAML（URL、method、headers、params、断言表达式），Python 层只负责加载与执行。新增接口用例不用写代码，改 YAML 即可。

**2. 接口依赖提取**
`extract.yaml` + `readyaml.py` 支持把上一个接口的响应字段提取出来，作为后续接口的入参（比如登录拿 token → 下单用 token），实现多接口串联。

**3. 分层封装**
- `sendrequest.py`：统一封装请求发送、日志、异常
- `assertions.py`：统一断言，支持 jsonpath 取值比对
- `connection.py`：MySQL 连接，用于接口后置的数据库校验

**4. 报告与通知**
- 支持 Allure：`run.py` 会跑用例 → 生成报告 → 自动打开
- `conftest.py` 里通过 `pytest_terminal_summary` 钩子统计通过/失败/跳过/耗时，并按开关推送钉钉群

**5. 运行环境隔离**
`report/`、`logs/`、`venv/`、`.idea/` 已在 `.gitignore` 排除，仓库只保留源码、用例数据与配置模板。

## 快速开始

```bash
git clone https://github.com/my-Qa/pytest-market.git
cd python_project

# Windows
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

按需修改 `conf/config.ini` 中的接口地址与数据库连接，然后：

```bash
python run.py                      # 跑全部用例 + 生成并打开 Allure 报告
pytest ./testcase -v               # 直接命令行跑
pytest ./testcase/Single\ interface -v   # 只跑单接口用例
```

> 生成 Allure 报告需要本机安装 Java 与 allure 命令行工具。

## 报告示例（终端摘要）

```
本次自动化测试执行完毕
用例总数：xx
通过：xx
失败：xx
异常：0
跳过：0
耗时：xx.xx s
```

## 后续规划

- [ ] 敏感配置（数据库密码、接口地址）改为环境变量读取
- [ ] 增加接口用例的 pytest 参数化，覆盖边界值与异常场景
- [ ] 统一断言模板，减少 YAML 中重复写法
- [ ] 接入 GitHub Actions，提交即跑接口回归
