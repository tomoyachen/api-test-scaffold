from common.request import Request

class PostMethodRequest(Request):
    def __init__(self, cookies = None):
        super().__init__(cookies)
        self.method = "POST"
        self.host = "https://httpbin.org"
        self.path = "/post"
        self.data = {
            "id": 1,
            "keywords": "",
            "code": 200,
            "message": None
        }
