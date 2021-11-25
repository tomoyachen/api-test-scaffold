from common.request import Request
from common.config import Config

class PostMethodRequest(Request):
    def __init__(self, cookies = None):
        super().__init__(cookies)
        self.method = "POST"
        self.host = Config.get_config("project_1_url")
        self.path = "/post"
        self.data = {
            "id": 1,
            "keywords": "",
            "code": 200,
            "message": None
        }
