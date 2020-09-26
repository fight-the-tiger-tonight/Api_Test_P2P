import random
import unittest
import requests
from parameterized import parameterized

from api.login_api_parameterized import LoginApi
from utils import read_imgcode_files


class TestGetImgVerifCode(unittest.TestCase):
    def setUp(self) -> None:
        self.loginapi = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 获取验证码方法
    @parameterized.expand(read_imgcode_files)
    def test_get_imgverifycode_success(self, type, status_code):
        if type == "float":
            r = str(random.random())
        elif type == "int":
            r = str(random.randint(100000, 9999999))
        elif type == "kong":
            r = ""
        elif type == "char":
            r = ''.join(random.sample("biagjkbskjnsd", 6))
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, r)
        self.assertEqual(status_code, response.status_code)
