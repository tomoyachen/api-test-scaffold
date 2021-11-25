import os
import platform
import yaml


class Config:

    @staticmethod
    def get_root_dir():
        def get_file_dir(file):
            o_path = os.getcwd()
            separator = '\\' if 'Windows' in platform.system() else '/'
            str = o_path
            str = str.split(separator)
            while len(str) > 0:
                spath = separator.join(str) + separator + file
                if os.path.exists(spath):
                    return os.path.dirname(spath)
                str.pop()
        return get_file_dir('conftest.py')

    @staticmethod
    def get_yaml(file_path) -> dict:
        with open(file_path, encoding="UTF-8") as f:
            data = yaml.load(f.read(), Loader=yaml.SafeLoader)
            return data
        return {}

    @staticmethod
    def set_environ(key: str, value: str):
        os.environ[key] = str(value)

    @staticmethod
    def get_environ(key: str):
        if key in [o_key for o_key in os.environ]:
            value = os.environ[key]
            try:
                value = int(value)
            except ValueError:
                if value == "True":
                    value = True
                elif value == "False":
                    value = False
            return value

    @classmethod
    def set_test_env(cls, environment):
        cls.set_environ("TEST_ENVIRONMENT", environment)

    @classmethod
    def get_test_env(cls):
        return cls.get_environ("TEST_ENVIRONMENT")

    @classmethod
    def get_configs(cls):
        environment = cls.get_test_env()
        configs_path = os.path.join(cls.get_root_dir(), 'config', f"{environment}.yaml")
        configs = cls.get_yaml(configs_path)
        return configs

    @classmethod
    def get_config(cls, key: str):
        configs = cls.get_configs()
        if key in configs:
            return configs[key]

    @classmethod
    def get_fixtures(cls, filename: str):
        environment = cls.get_test_env()
        fixtures_path = os.path.join(cls.get_root_dir(), 'fixtures', f"{environment}", f"{filename}.yaml")
        fixtures = cls.get_yaml(fixtures_path)
        return fixtures

    @classmethod
    def get_fixture(cls, filename: str, key: str):
        fixtures = cls.get_fixtures(filename)
        if key in fixtures:
            return fixtures[key]
