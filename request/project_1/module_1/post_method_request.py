from request.base_request import BaseRequest
from common.utils import Utils

class PostMethodRequest(BaseRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "POST"
        self.host = Utils.base_url
        self.path = "/post"
        self.data = {
            "id": 1,
            "keywords": "",
            "code": 200,
            "message": None
        }
