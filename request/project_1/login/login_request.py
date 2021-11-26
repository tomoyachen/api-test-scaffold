from common.request import Request
from common.config import Config

class LoginRequest(Request):
    def __init__(self, cookies = None):
        super().__init__(cookies)
        self.method = "POST"
        self.host = Config.get_config("project_1_url")
        self.path = "/post"
        self.data = {
            "username": "",
            "password": "",
            "code": 200, # 剧情需要
            "message": None # 剧情需要
        }

    def login_and_get_cookies(self, username, password):
        self.data["username"] = username
        self.data["password"] = password
        self.request()
        if self.is_success:
            self.response.cookies = {"_uuid": "12345678-AAAA-BBBB-CCCC-12345678ABCDEF12345678"} # 剧情需要
            return self.response.cookies