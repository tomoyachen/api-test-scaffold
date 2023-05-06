import pytest
import allure

from common.enums import UserType
from common.tools import Tools
from request.project_1.login.login_request import LoginRequest
from common.config import  Config

@allure.epic("Project 1")
@allure.feature("登录")
@allure.story("登录接口")
class LoginTest():

    @pytest.fixture(scope='function')
    def api(self):
        request = LoginRequest()
        user = Tools.get_user(UserType.NORMAL_USER)
        request.data["username"] = user["username"]
        request.data["password"] = user["password"]
        yield request

    @allure.title("成功请求")
    def test_login(self, api):

        api.request()
        api.asserts(expect_code=200)
