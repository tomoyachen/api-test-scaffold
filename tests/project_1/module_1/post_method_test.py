import pytest
import allure

from common.enums import UserType
from common.utils import Utils
from request.project_1.module_1.post_method_request import PostMethodRequest


@allure.epic("Project 1")
@allure.feature("Module 1")
@allure.story("Post 请求接口")
class PostMethodTest():

    @pytest.fixture(scope='function')
    def api(self):
        # 新的简洁登录方式，登录操作放在被测对象内部。
        # 好处是使用简单，坏处是如果一个测试框架有多个登录接口，需要做区分。
        # 已使用环境变量实现免登陆策略，同样是因为有免登录所以 scope=function，否则应该用class 并且做数据隔离。
        request = PostMethodRequest(user=Utils.get_user(UserType.NORMAL_USER))
        yield request

    @allure.title("成功请求")
    def test_post_method(self, api):

        api.request()
        api.asserts(expect_code=200)
        api.expect("$..id").to_equals(1)

    @allure.title("id 不存在")
    def test_post_method_with_id_not_exists(self, api):

        api.data['id'] = -1,
        api.data['code'] = 1001 # 剧情需要，mock 数据
        api.data['message'] = 'id 不存在' # 剧情需要，mock 数据
        api.request()
        api.asserts(expect_code=1001, expect_message='id 不存在')
