import logging
import unittest
import requests
from api.login_api_parameterized import LoginApi
from app import PHONE1
from utils import assert_utils, third_request_api


class TestLoan(unittest.TestCase):
    def setUp(self) -> None:
        self.loginapi = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 输入产品id，获取该投资产品详情
    def test01_get_loaninfo(self):
        # 认证成功的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response = {}".format(response.json()))
        # 获取存在的项目详情
        response = self.loginapi.loaninfo(self.session)
        logging.info("loaninfo-response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 获取不存在的项目
        response = self.loginapi.loaninfo(self.session, loan_id='999')
        logging.info("loaninfo-response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 输入金额进行投资
    def test02_tender_success(self):
        # 已充值的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 进行投资
        response = self.loginapi.tender(self.session)
        logging.info("loan response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 发送第三方投资接口请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("InitiativeTender OK", response.text)
        # 查询我的投资列表
        response = self.loginapi.mytenderlist(self.session)
        self.assertEqual(200, response.status_code)

    # 投资金额为空，投资失败
    def test03_tender_fail(self):
        # 已充值的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 进行投资
        response = self.loginapi.tender(self.session, amount='')
        logging.info("loan response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))

    # 投资金额为0，投资失败
    def test04_tender_fail(self):
        # 已充值的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 进行投资
        response = self.loginapi.tender(self.session, amount="0")
        logging.info("loan response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "投标金额不能低于最低投标金额")

    # 投资密码为空，投资失败
    def test05_tender_fail(self):
        # 已充值的账号登录
        phone = PHONE1
        response = self.loginapi.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 进行投资
        response = self.loginapi.tender(self.session, password="")
        logging.info("loan response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "投资密码不能为空")

    # 投资自己发的借款，投资失败
    def test06_tender_fail(self):
        # 已充值的账号登录
        response = self.loginapi.login(self.session, phone='13312345678', pwd='123456aa')
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 进行投资
        response = self.loginapi.tender(self.session)
        logging.info("loan response = {}".format(response.json()))
        assert_utils(self, response, 200, 100, "不能投自己的标")
        # 发送第三方投资接口请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("InitiativeTender OK", response.text)
