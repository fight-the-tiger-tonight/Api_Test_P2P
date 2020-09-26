import time
import unittest
import requests
from api.login_api import LoginApi


class TestLogin(unittest.TestCase):
    def setUp(self) -> None:
        self.loginapi = LoginApi()
        self.session = requests.Session()

    def tearDown(self) -> None:
        self.session.close()

    def test01_login_success(self):
        login_data = {"keywords": "18212345670", "password": "123456test"}
        response = self.loginapi.login(self.session, login_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("登录成功", response.json().get("description"))
        print(response.json().get("status"))
        print(response.json().get("description"))

    def test02_login_fail(self):
        login_data = {"keywords": "19212345670", "password": "123456test"}
        response = self.loginapi.login(self.session, login_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertEqual("用户不存在", response.json().get("description"))

    def test03_login_fail(self):
        login_data = {"keywords": "18212345671", "password": ""}
        response = self.loginapi.login(self.session, login_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertEqual("密码不能为空", response.json().get("description"))

    def test04_login_fail(self):
        login_data = {"keywords": "", "password": "123456test"}
        response = self.loginapi.login(self.session, login_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertEqual("用户名不能为空", response.json().get("description"))

    def test05_login_fail(self):
        login_data1 = {"keywords": "18212345673", "password": "1234"}
        # 第一次密码错误尝试登录
        response = self.loginapi.login(self.session, login_data1)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertEqual("密码错误1次,达到3次将锁定账户", response.json().get("description"))

        # 第二次密码错误尝试登录

        response = self.loginapi.login(self.session, login_data1)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertEqual("密码错误2次,达到3次将锁定账户", response.json().get("description"))

        # 第三次密码错误尝试登录

        response = self.loginapi.login(self.session, login_data1)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertEqual("由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录", response.json().get("description"))

        # 三次密码错误之后，输入正确用户名和密码，登录失败

        login_data2 = {"keywords": "18212345673", "password": "123456test"}
        response = self.loginapi.login(self.session, login_data2)
        self.assertEqual(200, response.status_code)
        self.assertEqual(100, response.json().get("status"))
        self.assertEqual("由于连续输入错误密码达到上限，账号已被锁定，请于1.0分钟后重新登录", response.json().get("description"))

        # 三次密码错误之后，1分钟解锁之后输入正确用户名和密码，登录成功
        time.sleep(61)
        response = self.loginapi.login(self.session, login_data2)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("登录成功", response.json().get("description"))

        # 判断是否登录
        response = self.loginapi.islogin(self.session)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.json().get("status"))
        self.assertEqual("OK", response.json().get("description"))

    # 未登录时，判断是否登录
    def test06_islogin_fail(self):
        response = self.loginapi.islogin(self.session)
        self.assertEqual(200, response.status_code)
        self.assertEqual(250, response.json().get("status"))
        self.assertEqual("您未登陆！", response.json().get("description"))
