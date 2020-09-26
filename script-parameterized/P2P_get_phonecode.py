import random
import unittest
import requests
from parameterized import parameterized

from api.login_api import LoginApi
from utils import read_param_data


class TestGetPhoneCode(unittest.TestCase):
    def setUp(self) -> None:
        self.loginapi = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()
    @parameterized.expand(read_param_data())
    def test01_get_phone_code_success(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        print(response.cookies)
        # 断言
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone_data = {"phone": "18212345670", "imgVerifyCode": "8888", "type": "reg"}
        response = self.loginapi.get_phonecode(self.session, phone_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertIn("短信发送成功", response.json().get("description"))
        print(response.cookies)


    def test02_get_phone_code_error(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        # 断言
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone_data = {"phone": "18212345670", "imgVerifyCode": "1111", "type": "reg"}
        response = self.loginapi.get_phonecode(self.session, phone_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertIn("图片验证码错误", response.json().get("description"))

    def test03_get_phone_code_error(self):
        # 先获取图片验证码

        # 获取短信验证码
        phone_data = {"phone": "18212345670", "imgVerifyCode": "8888", "type": "reg"}
        response = self.loginapi.get_phonecode(self.session, phone_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertIn("图片验证码错误", response.json().get("description"))

    def test04_get_phone_code_error(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        # 断言
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone_data = {"phone": "", "imgVerifyCode": "8888", "type": "reg"}
        response = self.loginapi.get_phonecode(self.session, phone_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    def test05_get_phone_code_error(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        # 断言
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone_data = {"phone": "18212345670", "imgVerifyCode": "", "type": "reg"}
        response = self.loginapi.get_phonecode(self.session, phone_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertIn("图片验证码错误", response.json().get("description"))
