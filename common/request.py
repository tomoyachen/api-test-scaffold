import requests
import json
import logging
import traceback

class Request():
    def __init__(self, cookies = None):
        self.method = "POST"
        self.url = None
        self.host = None
        self.path = None
        self.headers = {
            "content-type": "application/json; charset=utf-8"
        }
        self.cookies = cookies if cookies and isinstance(cookies, dict) else {}
        self.params = {}
        self.data = {}
        self.response = None


    def request(self):
        requests.packages.urllib3.disable_warnings()
        requests.adapters.DEFAULT_RETRIES = 5

        self.method = self.method.upper()
        self.url = self.url if self.url else self.host + self.path

        s = requests.session()
        s.keep_alive = False
        self.response = s.request(
            self.method,
            url=self.url,
            headers=self.headers,
            params=self.params,
            data=json.dumps(self.data),
            cookies=self.cookies,
            verify=False,
        )
        self.__log()

        return self.response


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

        log = logging.getLogger()
        log.info(f"""Caller: {traceback.extract_stack()[-3].__str__()}
{self.method}  {url_with_params}
Request Headers: {self.headers}
Request Body: {self.data}
HTTP Code: {self.response.status_code}
Response Body: {self.response.text}"""
                 )