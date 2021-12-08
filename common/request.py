import requests
import json
import logging
import traceback
import allure


class Request():
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
        self.response = None


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

        self.__log()
        self.is_success = True if self.response.json()["json"]["code"] == 200 else False

        return self.response

    @allure.step("断言")
    def assertion(self, expect_code = None, expect_message = None):
        if self.response is None:
            raise Exception("请先请求接口~")

        assert self.response.status_code == 200, f"HTTP CODE {self.response.status_code}"

        if expect_code is not None:
            assert expect_code == self.response.json()["json"]["code"], f"code 不一致"

        if expect_message  is not None:
            assert expect_message in self.response.json()["json"]["message"], f"message 不一致"

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

        from common.config import Config

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
            user_pool_str = Config.get_environ("PROJECT_1_USER_POOL")
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
                    Config.set_environ("PROJECT_1_USER_POOL", json.dumps(user_pool))
                    return cookies

    def __log(self):
        url_with_params = self.url
        if self.params:
            path = "&".join([f'{key}={self.params[key]}' for key in self.params])
            url_with_params += f"&{path}" if "?" in url_with_params else f"?{path}"

        from common.config import Config

        callers = []
        for item in traceback.extract_stack()[:-2]:
            if Config.get_root_dir() in item[0]:
                callers.append(item.__str__())

        log = logging.getLogger()
        nl = '\n'
        log.info(f"""Caller: {nl.join(callers)}
{self.method.upper()}  {url_with_params}
Cookies: {self.cookies}
Request Headers: {json.dumps(self.headers)}
Request Body: {json.dumps(self.data)}
HTTP Code: {self.response.status_code}
Response Body: {self.response.text}"""
                 )