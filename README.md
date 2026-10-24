# pytest-market

基于 `pytest` + `requests` + `PyYAML` + `Allure` 的接口自动化测试框架。

项目采用 YAML 数据驱动方式编写测试用例，支持单接口测试、业务流程测试、接口参数提取、动态参数替换和多种断言方式。

## 框架流程

```text
pytest
  -> fixture 前置处理
  -> 读取 YAML 测试数据
  -> 动态参数替换
  -> 发送 HTTP 请求
  -> 提取响应参数
  -> 执行断言
  -> 生成测试报告
```

## 核心功能

- YAML 数据驱动测试
- 支持单接口测试
- 支持多接口业务场景测试
- 支持 `GET`、`POST` 请求
- 支持 `params`、`data`、`json` 参数
- 支持 Cookie 和文件上传
- 支持 JSONPath、正则表达式提取响应参数
- 支持接口之间的参数传递
- 支持时间戳、日期、随机数据和加密参数
- 支持 `contains`、`eq`、`ne`、`rv`、`db` 断言
- 支持 Allure 和 JUnit 测试报告
- 支持日志记录和测试结果汇总

## 项目结构

```text
pytest-market/
├── base/                       # 测试执行器和基础工具
│   ├── apiutil.py              # 单接口执行器
│   ├── apiutil_business.py     # 业务场景执行器
│   └── new_testcase_tools.py   # 测试用例生成工具
├── common/                     # 公共方法
│   ├── sendrequest.py          # HTTP 请求封装
│   ├── assertions.py           # 断言封装
│   ├── readyaml.py             # YAML 解析
│   ├── debugtalk.py            # 动态参数函数
│   └── recordlog.py            # 日志封装
├── conf/                       # 环境和全局配置
├── data/                       # 测试数据
├── testcase/                   # 测试用例
│   ├── Single interface/       # 单接口测试
│   ├── Business interface/     # 业务流程测试
│   └── ProductManager/         # 商品管理测试
├── extract.yaml                # 接口依赖参数存储
├── conftest.py                 # 全局 fixture
├── pytest.ini                  # pytest 配置
├── requirements.txt            # 项目依赖
└── run.py                      # 项目运行入口
```

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置测试环境

修改：

```text
conf/config.ini
```

配置接口服务地址：

```ini
[api_envi]
host = http://127.0.0.1:8787
```

### 执行测试

运行全部测试：

```bash
pytest -s -v testcase
```

使用项目入口运行并生成 Allure 报告：

```bash
python run.py
```

生成 Allure 报告需要额外安装 Allure Commandline。

## 测试用例示例

```yaml
- baseInfo:
    api_name: 用户登录
    url: /dar/user/login
    method: post
    header:
      Content-Type: application/x-www-form-urlencoded;charset=UTF-8

  testCase:
    - case_name: 登录成功
      data:
        user_name: test01
        passwd: admin123
      validation:
        - contains:
            error_code: "0000"
        - eq:
            msg: 登录成功
      extract:
        token: $.token
```

## 接口参数关联

接口响应中的参数可以提取到 `extract.yaml`：

```yaml
extract:
  token: $.token
  orderNumber: $.orderNumber
```

后续接口通过占位符使用：

```yaml
json:
  token: ${get_extract_data(token)}
  orderNumber: ${get_extract_data(orderNumber)}
  timestamp: ${timestamp()}
```

## 内置示例

项目包含以下测试示例：

- 用户登录和用户管理
- 商品列表和商品详情
- 提交订单和订单支付
- 多接口业务流程测试
