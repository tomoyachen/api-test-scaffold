import pytest
import requests


class PostMethodTest:

    @staticmethod
    def test_post_method():
        url = "https://httpbin.org/post"
        headers = {
            'Content-Type': 'application/json'
        }
        body = {
            "id": 1,
            "keywords": ""
        }

        response = requests.request("POST", url, headers=headers, json=body)
        print(response.text)
        assert response.status_code == 200
        # assert response.json()["errCode"] == 200
