# -*- coding: utf-8 -*-
import time

import pytest

from common.readyaml import ReadYamlData
from base.removefile import remove_file
from common.dingRobot import send_dd_msg
from conf.setting import dd_msg

import warnings

yfd = ReadYamlData()


@pytest.fixture(scope="session", autouse=True)
def clear_extract():
    # 禁用HTTPS告警，ResourceWarning
    warnings.simplefilter('ignore', ResourceWarning)

    yfd.clear_yaml_data()
    remove_file("./report/temp", ['json', 'txt', 'attach', 'properties'])




start_time = 0

def pytest_sessionstart(session):
    global start_time
    start_time = time.time()

def generate_test_summary(terminalreporter):
    stats = terminalreporter.stats
    total = terminalreporter._numcollected
    passed = len(stats.get("passed", []))
    failed = len(stats.get("failed", []))
    error = len(stats.get("error", []))
    skipped = len(stats.get("skipped", []))
    duration = time.time() - start_time
    summary_text = (
        f"本次自动化测试执行完毕\n"
        f"用例总数：{total}\n"
        f"通过：{passed}\n"
        f"失败：{failed}\n"
        f"异常：{error}\n"
        f"跳过：{skipped}\n"
        f"耗时：{duration:.2f} s"
    )
    return summary_text

def pytest_terminal_summary(terminalreporter):
    summary = generate_test_summary(terminalreporter)
    print("\n" + summary)
    # 根据conf/setting.py中的dd_msg开关决定是否推送钉钉，发送失败不影响测试结果
    if dd_msg:
        from common.dingRobot import send_dd_msg
        try:
            send_dd_msg(summary)
        except Exception as e:
            print(f"钉钉消息发送失败，不影响测试结果：{e}")

