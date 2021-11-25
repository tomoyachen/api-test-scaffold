import pytest
import os
from common.config import Config

def pytest_addoption(parser): # 添加命令行参数
    parser.addoption("--env", action="store", dest="environment", default="dev", help="environment: dev, dev-01, dev-02")


def pytest_configure(config): # 初始化配置
    # 鉴于 PyCharm 单独执行用例总是在当前目录下生成报告，可以强制设定为根目录生成报告
    root_allure_report_dir = os.path.join(Config.get_root_dir(), config.getoption("allure_report_dir"))
    config.option.allure_report_dir = root_allure_report_dir

@pytest.fixture(scope="session", autouse=True)
def configs(pytestconfig): # 获取配置 & 写入 env (当前测试环境)
    environment = pytestconfig.getoption('environment')
    environment = environment if environment else 'dev'

    # env 写入环境变量
    Config.set_test_env(environment)

    config_path = os.path.join(pytestconfig.rootdir, "config", f"{environment}.yaml")
    yield Config.get_yaml(config_path)
