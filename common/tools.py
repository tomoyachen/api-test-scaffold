import os
import platform
import yaml


class Tools:

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
        return cls.get_environ("TEST_ENVIRONMENT") or "dev"

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
    def get_constants(cls, filename: str):
        environment = cls.get_test_env()
        constants_path = os.path.join(cls.get_root_dir(), 'constants', f"{environment}", f"{filename}.yaml")
        constants = cls.get_yaml(constants_path)
        return constants

    @classmethod
    def get_constant(cls, filename: str, key: str):
        constants = cls.get_constants(filename)
        if key in constants:
            return constants[key]

