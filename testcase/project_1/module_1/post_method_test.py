import pytest
from request.project_1.module_1.post_method_request import PostMethodRequest


class PostMethodTest():

    @pytest.fixture(scope='function')
    def api(self):
        request = PostMethodRequest()
        yield request

    def test_post_method(self, api):

        api.request()
        api.assertion(expect_code=200)


    def test_post_method_with_id_not_exists(self, api):

        api.data['id'] = -1,
        api.data['code'] = 1001 # 剧情需要
        api.data['message'] = 'id 不存在' # 剧情需要
        api.request()
        api.assertion(expect_code=1001, expect_message='id 不存在')
