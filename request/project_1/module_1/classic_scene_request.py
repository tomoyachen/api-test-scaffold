from common.request import Request
from common.config import Config
from common.db import Mysql

class ClassicSceneRequest(Request):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "POST"
        self.host = Config.get_config("project_1_url")
        self.path = "/post"
        self.data = {
            "id": 1,
            "status": 1,
            "code": 200, # 剧情需要，mock 数据
            "message": None # 剧情需要，mock 数据
        }

    def assertion(self, expect_code = None, expect_message = None, **extras):
        super().assertion(expect_code=expect_code, expect_message=expect_message)
        if self.is_success: # 业务上成功的接口，一般需要做额外的数据断言

            # 一般来源 1: 请求参数
            actual_status = self.response.json()["json"]["status"]
            expect_status = self.data["status"]
            assert actual_status == expect_status

            # 一般来源 2: 其他接口

            # 一般来源 3: 数据库
            # mysql = Mysql()
            # result = mysql.select_one("select * from s_link where id = 1")
            # actual_status_db = self.response.json()["json"]["status"]
            # expect_status_db = result["status"]
            # assert actual_status_db == expect_status_db

            # 接收自定义字段
            if "expect_custom_field" in extras:
                assert extras["expect_custom_field"] == "需要在断言中使用的内容"

    def get_user_last_article_id(self):
        self.data["id"] = 2
        self.request()
        if self.is_success and "id" in self.response.json()["json"]:
            return self.response.json()["json"]["id"]
