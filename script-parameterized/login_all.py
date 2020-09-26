import logging
import random
import time
import unittest
import requests

from api.login_api_parameterized import LoginApi
from app import PHONE1, PHONE2, PHONE3, PHONE4, PHONE5, PHONE6
from utils import assert_utils


class TestLoginAll(unittest.TestCase):
    def setUp(self) -> None:
        self.loginapi = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    # 定义获取验证码方法,随机数为小数
    def test01_get_imgverifycode_success(self):
        r = random.random()
        print(r)
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        # 断言
        self.assertEqual(200, response.status_code)

    # 随机数为整数
    def test02_get_imgverifycode_success(self):
        r = random.randint(10000, 999999)
        print(r)
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        # 断言
        self.assertEqual(200, response.status_code)

    # 随机数为空
    def test03_get_imgverifycode_None(self):
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, "")
        # 断言
        self.assertEqual(404, response.status_code)

    # 随机数为字母
    def test04_get_imgverifycode_error(self):
        r_list = random.sample("ndjhiubjnkn", 7)
        r = "".join(r_list)
        print(r)
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, r)
        # 断言
        self.assertEqual(400, response.status_code)

    # 获取短信验证码成功
    def test05_get_phone_code_success(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        # 断言
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE1
        response = self.loginapi.get_phonecode(self.session, phone)
        # 断言
        assert_utils(self, response, 200, 200, "短信发送成功")
        print(response.json())

    # 获取短信验证码失败，图片验证码错误
    def test06_get_phone_code_error(self):
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

    # 获取短信验证码失败，未获取图片验证码
    def test07_get_phone_code_error(self):
        # 先获取图片验证码

        # 获取短信验证码
        phone_data = {"phone": "18212345670", "imgVerifyCode": "8888", "type": "reg"}
        response = self.loginapi.get_phonecode(self.session, phone_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertIn("图片验证码错误", response.json().get("description"))

    # 获取短信验证码失败，手机号为空
    def test08_get_phone_code_error(self):
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

    # 获取短信验证码失败，图片验证码为空
    def test09_get_phone_code_error(self):
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

    # 填写所有必填参数，注册成功
    def test01_register_success(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE1
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone)
        assert_utils(self, response, 200, 200, "注册成功")
        logging.info("register-response{}".format(response.json()))

    # 填写所有全部参数，注册成功
    def test02_register_success(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE2
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, "13312345678")
        assert_utils(self, response, 200, 200, "注册成功")
        logging.info("register-response{}".format(response.json()))

    # 图片验证码为空，注册失败
    def test03_register_fail(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        # 断言
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE3
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, imgcode='')
        assert_utils(self, response, 200, 100, "短信验证码不能为空")
        logging.info("register-response{}".format(response.json()))

    # 短信验证码为空，注册失败
    def test04_register_fail(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE3
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, phone_code="")
        assert_utils(self, response, 200, 100, "验证码不能为空!")
        logging.info("register-response{}".format(response.json()))

    # 图片验证码错误时，注册失败
    def test05_register_fail(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        # 断言
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE3
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, imgcode='1111')
        assert_utils(self, response, 200, 100, "验证码错误!")
        logging.info("register-response{}".format(response.json()))

    # 短信验证码错误时，注册失败
    def test06_register_fail(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE3
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, phone_code='555555')
        assert_utils(self, response, 200, 100, "验证码错误")
        logging.info("register-response{}".format(response.json()))

    # 手机号已存在时，注册失败
    def test07_register_fail(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE1
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone)
        assert_utils(self, response, 200, 100, "手机已存在!")
        logging.info("register-response{}".format(response.json()))

    # 密码为空时，注册失败
    def test08_register_fail(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE3
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, pwd='')
        assert_utils(self, response, 200, 100, "密码不能为空")
        logging.info("register-response{}".format(response.json()))

    # 不同意注册条款时，注册失败
    def test09_register_fail(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE4
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, dy_server='off')
        assert_utils(self, response, 200, 100, "请同意我们的条款")
        logging.info("register-response{}".format(response.json()))

    # 邀请人手机号错误，注册失败
    def test10_register_fail(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE5
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone, invite_phone="error")
        assert_utils(self, response, 200, 100, "推荐人不存在")
        logging.info("register-response{}".format(response.json()))

    # 填写所有必填参数，注册成功（备用注册手机号码）
    def test11_register_success(self):
        # 先获取图片验证码
        r = random.random()
        # 调用图片验证码接口
        response = self.loginapi.get_imgverifycode(self.session, str(r))
        self.assertEqual(200, response.status_code)
        # 获取短信验证码
        phone = PHONE6
        response = self.loginapi.get_phonecode(self.session, phone)
        assert_utils(self, response, 200, 200, "短信发送成功")
        # 注册请求
        response = self.loginapi.register(self.session, phone)
        assert_utils(self, response, 200, 200, "注册成功")
        logging.info("register-response{}".format(response.json()))

    # 登录成功
    def test01_login_success(self):
        # 登录请求
        phone = PHONE1
        response = self.loginapi.login(self.session,phone)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))

    # 登录失败，未注册账号
    def test02_login_fail(self):
        response = self.loginapi.login(self.session, phone='19856231254')
        assert_utils(self, response, 200, 100, "用户不存在")
        logging.info("login-response{}".format(response.json()))

    # 登录失败，密码为空
    def test03_login_fail(self):
        response = self.loginapi.login(self.session, pwd="")
        assert_utils(self, response, 200, 100, "密码不能为空")
        logging.info("login-response{}".format(response.json()))

    # 登录失败，手机号账号
    def test04_login_fail(self):
        response = self.loginapi.login(self.session, "")
        assert_utils(self, response, 200, 100, "用户名不能为空")
        logging.info("login-response{}".format(response.json()))

    # 登录失败，密码错误
    def test05_login_fail(self):
        # 第一次密码错误尝试登录
        response = self.loginapi.login(self.session, pwd="123")
        assert_utils(self, response, 200, 100, "密码错误1次,达到3次将锁定账户")
        logging.info("login-response{}".format(response.json()))

        # 第二次密码错误尝试登录
        response = self.loginapi.login(self.session, pwd="123")
        assert_utils(self, response, 200, 100, "密码错误2次,达到3次将锁定账户")
        logging.info("login-response{}".format(response.json()))

        # 第三次密码错误尝试登录
        response = self.loginapi.login(self.session, pwd="123")
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        logging.info("login-response{}".format(response.json()))

        # 三次密码错误之后，输入正确用户名和密码，登录失败
        response = self.loginapi.login(self.session)
        assert_utils(self, response, 200, 100, "由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录")
        logging.info("login-response{}".format(response.json()))

        # 三次密码错误之后，1分钟解锁之后输入正确用户名和密码，登录成功
        time.sleep(61)
        response = self.loginapi.login(self.session)
        assert_utils(self, response, 200, 200, "登录成功")
        logging.info("login-response{}".format(response.json()))

        # 判断是否登录
        response = self.loginapi.islogin(self.session)
        assert_utils(self, response, 200, 200, "OK")
        logging.info("login-response{}".format(response.json()))

    # 未登录时，判断是否登录
    def test06_islogin_fail(self):
        response = self.loginapi.islogin(self.session)
        assert_utils(self, response, 200, 250, "您未登陆！")
        logging.info("login-response{}".format(response.json()))
