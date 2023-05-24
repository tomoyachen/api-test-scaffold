import pytest
import os
from common.tools import Tools
import logging
import requests
import allure

def pytest_addoption(parser): # 添加命令行参数
    parser.addoption("--env", action="store", dest="environment", default="dev", help="environment: dev, dev-01, dev-02")


def pytest_configure(config): # 初始化配置
    # 鉴于 PyCharm 单独执行用例总是在当前目录下生成报告，可以强制设定为根目录生成报告
    root_allure_report_dir = os.path.join(Tools.get_root_dir(), config.option.allure_report_dir)
    config.option.allure_report_dir = root_allure_report_dir

@pytest.fixture(scope="session", autouse=True)
def configs(pytestconfig): # 获取配置 & 写入 env (当前测试环境)
    environment = pytestconfig.getoption('environment')
    environment = environment if environment else 'dev'

    # env 写入环境变量
    Tools.set_test_env(environment)

    config_path = os.path.join(pytestconfig.rootdir, "config", f"{environment}.yaml")
    yield Tools.get_yaml(config_path)


@pytest.fixture(scope="class")
def login():
    @allure.step("登录")
    def __login(username, password) -> requests.cookies.RequestsCookieJar:
        prev_user_key = username + password
        log = logging.getLogger()

        if hasattr(login, "cookies"): # 同一用户免登录策略
            if prev_user_key in login.cookies and login.cookies[prev_user_key]:
                log.info(f'用户 {username} 免登录')
                return login.cookies[prev_user_key]
        else:
            login.cookies = {}

        from request.project_1.login.login_request import LoginRequest
        api = LoginRequest()
        cookies = api.login_and_get_cookies(username, password)

        if cookies:
            login.cookies[prev_user_key] = cookies # 如果登录成功，cookies 存入用户池
            log.info(f'用户 {username} 登录成功')
            return cookies

        log.info(f'用户 {username} 登录失败 或 登录接口未返回 cookies')
        return cookies

    yield __login


@pytest.fixture(scope="class")
def login_with_user(login):
    def __login_with_user(user: dict) -> str:
        if isinstance(user, dict) and 'username' in user and 'password' in user:
            return login(user['username'], user['password'])

    yield __login_with_user
