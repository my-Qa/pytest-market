import logging
import os
import sys

DIR_BASE = os.path.dirname(os.path.dirname(__file__))
sys.path.append(DIR_BASE)

# log日志输出级别
LOG_LEVEL = logging.DEBUG  # 文件
STREAM_LOG_LEVEL = logging.DEBUG  # 控制台

# 接口超时时间，单位/s
API_TIMEOUT = 60

# 测试报告类型，当前支持allure
REPORT_TYPE = 'allure'

# 是否发送钉钉消息
dd_msg = True

# 文件路径
FILE_PATH = {
    'CONFIG': os.path.join(DIR_BASE, 'conf/config.ini'),
    'LOG': os.path.join(DIR_BASE, 'logs'),
    'YAML': os.path.join(DIR_BASE),
    'TEMP': os.path.join(DIR_BASE, 'report/temp'),
    'EXTRACT': os.path.join(DIR_BASE, 'extract.yaml'),
    'RESULTXML': os.path.join(DIR_BASE, 'report')
}

# 默认请求头信息
LOGIN_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive'
}
