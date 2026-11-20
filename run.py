import os
import shutil

import pytest

from conf.setting import REPORT_TYPE

if __name__ == '__main__':

    if REPORT_TYPE == 'allure':
        pytest.main(
            ['-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir',
             '--junitxml=./report/results.xml'])

        shutil.copy('./environment.xml', './report/temp')
        os.system(f'allure serve ./report/temp')
