import logging
import time
import unittest
import requests
from api.login_api_parameterized import LoginApi
from app import PHONE1, PHONE2, PHONE3, PHONE4
from utils import assert_utils


class TestApprove(unittest.TestCase):
    def setUp(self) -> None:
        self.loginapi = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 正确姓名和身份证号，提交成功
    def test01_pprove_success(self):
        # 先登录账号
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 提交认证
        response = self.loginapi.approve(self.session, "甘道夫", "440307199008077699")
        assert_utils(self, response, 200, 200, "提交成功!")
        logging.info("login-response{}".format(response.json()))

        # 发送获取认证信息请求
        response = self.loginapi.get_approve(self.session)
        self.assertEqual(200, response.status_code)

    # 姓名为空，提交失败
    def test02_pprove_fail(self):
        # 先登录账号
        phone = PHONE2
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 提交认证
        response = self.loginapi.approve(self.session, "", "440307199008077699")
        assert_utils(self, response, 200, 100, "姓名不能为空")
        logging.info("login-response{}".format(response.json()))

    # 身份证号为空，提交失败
    def test03_pprove_fail(self):
        # 先登录账号
        phone = PHONE2
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 提交认证
        response = self.loginapi.approve(self.session, "甘道夫", "")
        assert_utils(self, response, 200, 100, "身份证号不能为空")
        logging.info("login-response{}".format(response.json()))

    # 身份证号错误，提交失败
    def test04_pprove_fail(self):
        # 先登录账号
        phone = PHONE3
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 提交认证
        response = self.loginapi.approve(self.session, "甘道夫", "error")
        assert_utils(self, response, 200, 100, "身份证号不能为空")
        logging.info("login-response{}".format(response.json()))

    # 已认证身份证号，提交失败
    def test05_pprove_fail(self):
        # 先登录账号
        phone = PHONE4
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 提交认证
        response = self.loginapi.approve(self.session, "王富贵", "440307199008077699")
        assert_utils(self, response, 200, 100, "重复")
        logging.info("login-response{}".format(response.json()))
