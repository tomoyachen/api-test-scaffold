import pytest
import allure
from request.project_1.module_1.post_method_request import PostMethodRequest

@allure.epic("Project 1")
@allure.feature("Module 1")
@allure.story("Post 请求接口")
class PostMethodTest():

    @pytest.fixture(scope='function')
    def api(self):
        request = PostMethodRequest()
        yield request

    @allure.title("成功请求")
    def test_post_method(self, api):

        api.request()
        api.assertion(expect_code=200)

    @allure.title("id 不存在")
    def test_post_method_with_id_not_exists(self, api):

        api.data['id'] = -1,
        api.data['code'] = 1001 # 剧情需要
        api.data['message'] = 'id 不存在' # 剧情需要
        api.request()
        api.assertion(expect_code=1001, expect_message='id 不存在')
