import curlify
import requests
import json
import logging
import allure
from jsonpath import jsonpath
from common.expect import Expect
import _io

class BaseRequest():
    def __init__(self, cookies: requests.cookies.RequestsCookieJar = None, user: dict = None):
        self.method = "POST"
        self.url = None
        self.host = None
        self.path = None
        self.headers = {
            "content-type": "application/json; charset=utf-8"
        }
        self.cookies = cookies if cookies or not user else self.__login_and_get_cookies(user) # cookies 优先
        self.params = {}
        self.data = {}
        self.response: requests.models.Response = None


    def request(self):
        @allure.step(f"请求 {self.path}")
        def __request_and_get_response(info:dict = self.__dict__) -> requests.models.Response: # 不需要传入参数，纯粹为了 allure 报告好看
            return s.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                params=self.params,
                data=json.dumps(self.data),
                cookies=self.cookies,
                verify=False
            )

        requests.packages.urllib3.disable_warnings()
        requests.adapters.DEFAULT_RETRIES = 5

        self.url = self.url if self.url else self.host + self.path

        s = requests.session()
        s.keep_alive = False
        self.response = __request_and_get_response()

        self.__network_log()
        self.is_success = True if self.response_json() and self.response_json().get("json").get("code") == 200 else False

        return self.response

    def response_json(self):
        try:
            return self.response.json()
        except:
            return {}

    @allure.step("断言")
    def asserts(self, expect_code = None, expect_message = None, expect_httpcode = 200):
        if self.response is None:
            raise Exception("请先请求接口~")

        assert self.response.status_code == expect_httpcode, f"HTTP CODE {self.response.status_code}"

        if expect_code is not None:
            assert expect_code == self.response.json()["json"]["code"], f"errCode 不一致"

        if expect_message  is not None:
            assert expect_message in self.response.json()["json"]["message"], f"message 不一致"


    @allure.step("断言")
    def expect(self, response_expr) -> Expect:
        results = jsonpath(self.response.json(), response_expr)
        if results and len(results) > 0:
            return Expect(results[0])

    @allure.step("登录")
    def __login_and_get_cookies(self, user: dict):
        def __str_to_cookies(cookies_str: str) -> requests.cookies.RequestsCookieJar:
            cookies_rcj = requests.cookies.RequestsCookieJar()
            for cookie_kv in cookies_str.split(";"):
                cookie = cookie_kv.split("=")
                cookies_rcj.__setitem__(cookie[0].strip(), cookie[1].strip())
            return cookies_rcj

        def __cookies_to_str(cookies_rcj: requests.cookies.RequestsCookieJar) -> str:
            return "; ".join([str(key) + "=" + str(value) for key,value in cookies_rcj.items()])

        from common.tools import Tools

        if not isinstance(user, dict):
            return

        if not "site" in user:
            user["site"] = "project_1"

        log = logging.getLogger()
        # 如果是 project_1 用户
        if user["site"].lower() == "project_1" and "username" in user and "password" in user:
            username = user["username"]
            password = user["password"]
            prev_user_key = username + password
            user_pool_str = Tools.get_environ("PROJECT_1_USERS")
            user_pool = json.loads(user_pool_str) if user_pool_str else {}
            if prev_user_key in user_pool and user_pool[prev_user_key]:
                log.info(f'用户 {username} 免登录')
                cookies_rcj = __str_to_cookies(user_pool[prev_user_key]) # 取的适合转成 rcj
                return cookies_rcj
            else:
                from request.project_1.login.login_request import LoginRequest
                cookies = LoginRequest().login_and_get_cookies(username, password)
                if cookies:
                    log.info(f'用户 {user["phone"]} 登录成功')
                    user_pool[prev_user_key] = __cookies_to_str(cookies) # 存的时候转成 string
                    Tools.set_environ("PROJECT_1_USERS", json.dumps(user_pool))
                    return cookies

    def __network_log(self):

        url_with_params = self.url
        if self.params:
            path = "&".join([f'{key}={self.params[key]}' for key in self.params])
            url_with_params += f"&{path}" if "?" in url_with_params else f"?{path}"

        if isinstance(self.response.request.body, dict):
            request_data = json.dumps(self.response.request.body, ensure_ascii=False)
        elif isinstance(self.response.request.body, _io.BufferedReader):
            request_data = '二进制数据，不宜展示'
        elif isinstance(self.response.request.body, str):
            request_data = self.response.request.body
        else:
            request_data = '无法展示'

        content_type = self.response.headers['Content-Type']

        if 'application/json' in content_type:
            try:
                response_data = json.dumps(self.response.json(), ensure_ascii=False)
            except ValueError:
                response_data = "无法解析 JSON 响应"
        elif 'text/html' in content_type:
            response_data = "HTML 响应，不宜展示"
        elif 'application/octet-stream' in content_type:
            response_data = '二进制响应，不宜展示'
        else:
            response_data = '未知的响应类型'

        log = logging.getLogger()

        log.info("=========== network start ===========")
        log.info(f"{self.method.upper()} {url_with_params}")
        log.info("Request Headers: " + json.dumps(self.headers, ensure_ascii=False))
        log.info("Request Body: " + request_data)
        log.info("HTTP Code: " + str(self.response.status_code))
        log.info("Response Body: " + response_data)
        if not isinstance(self.response.request.body, _io.BufferedReader):
            log.info("=========== cURL ===========")
            log.info(curlify.to_curl(self.response.request)) # 泄露 cookies 风险，不建议使用
        log.info("=========== network end ===========")

