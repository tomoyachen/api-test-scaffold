import pytest
import allure
from request.project_1.login.login_request import LoginRequest
from common.config import  Config

@allure.epic("Project 1")
@allure.feature("登录")
@allure.story("登录接口")
class LoginTest():

    @pytest.fixture(scope='function')
    def api(self):
        request = LoginRequest()
        user = Config.get_fixture("project_1", "normal_user")
        request.data["username"] = user["username"]
        request.data["password"] = user["password"]
        yield request

    @allure.title("成功请求")
    def test_login(self, api):

        api.request()
        api.assertion(expect_code=200)
