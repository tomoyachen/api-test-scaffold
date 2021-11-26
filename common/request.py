import requests
import json
import logging
import traceback
import allure


class Request():
    def __init__(self, cookies: requests.cookies.RequestsCookieJar = None):
        self.method = "POST"
        self.url = None
        self.host = None
        self.path = None
        self.headers = {
            "content-type": "application/json; charset=utf-8"
        }
        self.cookies = cookies if cookies else None
        self.params = {}
        self.data = {}
        self.response = None


    # @allure.step("请求")
    def request(self):
        requests.packages.urllib3.disable_warnings()
        requests.adapters.DEFAULT_RETRIES = 5

        self.url = self.url if self.url else self.host + self.path

        s = requests.session()
        s.keep_alive = False
        with allure.step(f"请求 {self.path}"): # 为了显示 path，因为没有入参，所以不能用装饰器
            self.response = s.request(
                method=self.method,
                url=self.url,
                headers=self.headers,
                params=self.params,
                data=json.dumps(self.data),
                cookies=self.cookies,
                verify=False,
            )
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
Request Headers: {json.dumps(self.headers)}
Request Body: {json.dumps(self.data)}
HTTP Code: {self.response.status_code}
Response Body: {self.response.text}"""
                 )