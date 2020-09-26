import logging
import random
import unittest
import requests
from api.login_api_parameterized import LoginApi
from app import PHONE_x
from utils import assert_utils, third_request_api, DBUtils


class Business_Process_Loan(unittest.TestCase):
    def setUp(self) -> None:
        self.hmlc_api = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    @classmethod
    def tearDownClass(cls) -> None:
        sql1 = "delete log.* from mb_member_login_log log inner join mb_member ber on log.member_id = ber.id where log.member_name = '18212345676';"
        DBUtils.execute_sql(sql1)
        sql2 = "delete reg.* from mb_member_register_log reg inner join mb_member ber on reg.member_name = ber.phone where reg.phone = '18212345676';"
        DBUtils.execute_sql(sql2)
        sql3 = "delete fo.* from mb_member_info fo left join mb_member ber on fo.member_id = ber.id where fo.member_name = '18212345676';"
        DBUtils.execute_sql(sql3)
        sql4 = "delete from mb_member where name = '18212345676';"
        DBUtils.execute_sql(sql4)

    def test01_business_process_loan_success(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.hmlc_api.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE_x
        response = self.hmlc_api.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.hmlc_api.register(self.session, phone)
        assert_utils(self, response, 200, 200, "注册成功")
        logging.info("register-response{}".format(response.json()))
        # 登录请求
        phone = PHONE_x
        response = self.hmlc_api.login(self.session, phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))
        # 提交认证
        response = self.hmlc_api.approve(self.session, "胡翠花", "320412198409047436")
        assert_utils(self, response, 200, 200, "提交成功!")
        logging.info("login-response{}".format(response.json()))
        # 发送获取认证信息请求
        response = self.hmlc_api.get_approve(self.session)
        self.assertEqual(200, response.status_code)
        # 发送开户请求
        response = self.hmlc_api.account(self.session)
        logging.info("account response={}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 发送第三方开户接口请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("UserRegister OK", response.text)
        # 获取验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.hmlc_api.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 进行充值
        response = self.hmlc_api.recharge(self.session, "100")
        logging.info("recharge response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 发送第三方充值接口请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("NetSave OK", response.text)
        # 获取存在的项目详情
        response = self.hmlc_api.loaninfo(self.session)
        logging.info("loaninfo-response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 进行投资
        response = self.hmlc_api.tender(self.session)
        logging.info("loan response = {}".format(response.json()))
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        # 发送第三方投资接口请求
        form_data = response.json().get("description").get("form")
        response = third_request_api(form_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("InitiativeTender OK", response.text)
        # 查询我的投资列表
        response = self.hmlc_api.mytenderlist(self.session)
        self.assertEqual(200, response.status_code)
