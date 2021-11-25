import pytest
import os
import yaml

def pytest_addoption(parser): # 添加命令行参数
    parser.addoption("--env", action="store", dest="environment", default="dev", help="environment: dev, dev-01, dev-02")

@pytest.fixture(scope="session", autouse=True)
def configs(pytestconfig): # 获取配置 & 写入 env (当前测试环境)
    environment = pytestconfig.getoption('environment')
    environment = environment if environment else 'dev'

    # env 写入环境变量
    from common.config import Config
    Config.set_test_env(environment)

    config_path = os.path.join(pytestconfig.rootdir, "config", f"{environment}.yaml")
    yield Config.get_yaml(config_path)
