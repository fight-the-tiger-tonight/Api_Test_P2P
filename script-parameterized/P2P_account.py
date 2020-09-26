import logging
import random
import time
import unittest
import requests
from bs4 import BeautifulSoup
from api.login_api_parameterized import LoginApi
from app import PHONE1
from utils import assert_utils, third_request_api


class TestAccount(unittest.TestCase):
    def setUp(self) -> None:
        self.loginapi = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    def test01_account_success(self):
        # 认证成功的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 发送开户请求
        response = self.loginapi.account(self.session)
        logging.info("account response={}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 发送第三方开户接口请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)

    # 填写所有全部参数，充值成功
    def test02_recharge_success(self):
        # 认证成功的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 获取验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 进行充值
        response = self.loginapi.recharge(self.session, "100")
        logging.info("recharge response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 发送第三方充值接口请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("NetSave OK", response.text)

    # 验证码错误，充值失败
    def test03_recharge_fail(self):
        # 认证成功的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 获取验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 进行充值
        response = self.loginapi.recharge(self.session, "100", code='1111')
        assert_utils(self, response, 200, 100, "验证码错误")
        logging.info("recharge response = {}".format(response.json()))

    # 验证码为空，充值失败
    def test04_recharge_fail(self):
        # 认证成功的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 获取验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 进行充值
        response = self.loginapi.recharge(self.session, "100", code='')
        assert_utils(self, response, 200, 100, "验证码错误")
        logging.info("recharge response = {}".format(response.json()))

    # 输入金额为0，充值失败
    def test05_recharge_fail(self):
        # 认证成功的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 获取验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 进行充值
        response = self.loginapi.recharge(self.session, "0")
        assert_utils(self, response, 200, 100, "充值金额必须大于0")
        logging.info("recharge response = {}".format(response.json()))

    # 充值金额为空
    def test06_recharge_fail(self):
        # 认证成功的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 获取验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 进行充值
        response = self.loginapi.recharge(self.session, "")
        assert_utils(self, response, 200, 100, "充值金额不能为空")
        logging.info("recharge response = {}".format(response.json()))
