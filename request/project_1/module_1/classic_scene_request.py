from common.request import Request
from common.config import Config

class ClassicSceneRequest(Request):
    def __init__(self, cookies = None):
        super().__init__(cookies)
        self.method = "POST"
        self.host = Config.get_config("project_1_url")
        self.path = "/post"
        self.data = {
            "id": 1,
            "status": 1,
            "code": 200, # 剧情需要
            "message": None # 剧情需要
        }

    def assertion(self, expect_code = None, expect_message = None):
        super().assertion(expect_code=expect_code, expect_message=expect_message)
        if self.is_success: # 业务上成功的接口，一般需要做额外的数据断言

            # 一般来源 1: 请求参数
            actual_status = self.response.json()["json"]["status"]
            expect_status = self.data["status"]
            assert actual_status == expect_status

            # 一般来源 2: 其他接口
            # 一般来源 3: 数据库

    def get_user_last_article_id(self):
        self.data["id"] = 2
        self.request()
        if self.is_success and "id" in self.response.json()["json"]:
            return self.response.json()["json"]["id"]