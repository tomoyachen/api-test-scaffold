import pytest
import allure
from request.project_1.module_1.classic_scene_request import ClassicSceneRequest
from common.config import Config

@allure.epic("Project 1")
@allure.feature("Module 1")
@allure.story("经典场景示例接口")
class ClassicSceneTest():

    @pytest.fixture(scope='function')
    def api(self, login):
        user = Config.get_fixture("project_1", "normal_user")
        user_cookies = login(username=user["username"], password=user["password"])
        request = ClassicSceneRequest(cookies=user_cookies) # 带上登录态
        yield request

    @pytest.fixture(scope='function')
    def last_article_id(self, api):
        # 也可以不通过 fixtures 的方式来获取动态数据，但 allure 报告中会出现在 Test body 中
        yield ClassicSceneRequest(cookies=api.cookies).get_user_last_article_id()

    @allure.title("成功请求")
    @allure.severity("critical") # 优先级（blocker, critical, normal, minor, trivial）
    @pytest.mark.p0 # 标记用于分组执行
    def test_classic_scene(self, api):
        """测试用例的详细描述可以写在这里"""

        api.request()
        api.assertion(expect_code=200)

    @allure.title("动态获取数据")
    @pytest.mark.p1
    def test_classic_scene_with_dynamic_data(self, api, last_article_id):

        api.data["id"] = last_article_id
        api.request()
        api.assertion(expect_code=200)

    @allure.title("参数化 status: {status}")
    @pytest.mark.p1
    @pytest.mark.parametrize('status', [-1, 0, 1], ids=["异常","无效","有效"])
    def test_classic_scene_with_parametrize(self, api, status):

        api.data["status"] = status
        api.request()
        api.assertion(expect_code=200)