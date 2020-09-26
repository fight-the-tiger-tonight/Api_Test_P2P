import logging
import random
import unittest
import requests
from parameterized import parameterized
from api.login_api_parameterized import LoginApi
from utils import assert_utils, read_register_files, DBUtils, read_param_data


class TestRegister(unittest.TestCase):
    def setUp(self) -> None:
        self.loginapi = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 注册请求
    # @parameterized.expand(read_register_files)
    @parameterized.expand(read_param_data("register.json", "test_register",
                                          "phone,pwd,verifycode,phone_code,dy_server,invitephone,status_code,status,description"))
    def test_register_success(self, phone, pwd, imgcode, phone_code, dy_server, invite_phone, status_code, status,
                              description):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(status_code, response.status_code)
        # 获取短信验证码
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, pwd, imgcode, phone_code, dy_server, invite_phone)
        assert_utils(self, response, status_code, status, description)
        logging.info("register-response{}".format(response.json()))

    @classmethod
    def setUpClass(cls) -> None:
        sql1 = "delete log.* from mb_member_login_log log inner join mb_member ber on log.member_id = ber.id where log.member_name in ('18212345670','18212345671','18212345672','18212345673','18212345674','18212345675','18212345676');"
        DBUtils.execute_sql(sql1)
        logging.info("sql1={}".format(sql1))
        sql2 = "delete reg.* from mb_member_register_log reg inner join mb_member ber on reg.member_name = ber.phone where reg.phone in ('18212345670','18212345671','18212345672','18212345673','18212345674','18212345675','18212345676');"
        DBUtils.execute_sql(sql2)
        logging.info("sql2={}".format(sql2))
        sql3 = "delete fo.* from mb_member_info fo left join mb_member ber on fo.member_id = ber.id where fo.member_name in ('18212345670','18212345671','18212345672','18212345673','18212345674','18212345675','18212345676');"
        DBUtils.execute_sql(sql3)
        logging.info("sql3={}".format(sql3))
        sql4 = "delete from mb_member where name in ('18212345670','18212345671','18212345672','18212345673','18212345674','18212345675','18212345676');"
        DBUtils.execute_sql(sql4)
        logging.info("sql4={}".format(sql4))
