from request.base_request import BaseRequest
from common.utils import Utils

class LoginRequest(BaseRequest):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.method = "POST"
        self.host = Utils.base_url
        self.path = "/post"
        self.data = {
            "username": "",
            "password": "",
            "code": 200, # 剧情需要，mock 数据
            "message": None # 剧情需要，mock 数据
        }

    def login_and_get_cookies(self, username, password):
        self.data["username"] = username
        self.data["password"] = password
        self.request()
        if self.is_success:
            # 本示例使用的是 requests 库内置的 cookies 对象，相对稳定但复杂。
            # 有兴趣的也可以改为在 headers 里传递 cookies 字符串（=号连接 ;号分割的格式），转换语句如下：
            # cookies_str = "; ".join([str(key) + "=" + str(value) for key,value in cookies_rcj.items()])
            self.response.cookies.__setitem__("_uuid", "12345678-AAAA-BBBB-CCCC-12345678ABCDEF12345678") # 剧情需要，mock 数据
            return self.response.cookies