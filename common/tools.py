import json
import random
import time
from common.config import Config
from common.enums import UserType, ProjectType

class Tools():

    @classmethod
    def get_user(cls, user_type: UserType = UserType.NORMAL_USER):
        return Config.get_fixture(ProjectType.PROJECT_1.value, user_type.value)


    # def get_new_user(self):
    #     # your code ...
    #     return new_user


    @staticmethod
    def generate_salt(len = 8):
        import random
        import string
        salt = ''.join(random.sample(string.ascii_letters + string.digits, len))
        return salt
