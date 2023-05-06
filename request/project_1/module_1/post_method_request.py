from common.base_request import BaseRequest
from common.config import Config

class PostMethodRequest(BaseRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "POST"
        self.host = Config.get_config("project_1_url")
        self.path = "/post"
        self.data = {
            "id": 1,
            "keywords": "",
            "code": 200,
            "message": None
        }
