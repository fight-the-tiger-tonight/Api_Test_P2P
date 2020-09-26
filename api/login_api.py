import requests

from app import BASE_URL


class LoginApi:
    def __init__(self):
        self.img_verify_code_url = BASE_URL + "/common/public/verifycode1/"
        self.phone_code_url = BASE_URL + "/member/public/sendSms"
        self.register_url = BASE_URL + "/member/public/reg"
        self.login_url = BASE_URL + "/member/public/login"
        self.islogin_url = BASE_URL + "/member/public/islogin"
        self.approve_url = BASE_URL + "/member/realname/approverealname"
        self.get_approve_url = BASE_URL + "/member/member/getapprove"
        self.account_url = BASE_URL + "/trust/trust/register"
        self.loaninfo_url = BASE_URL + "/common/loan/loaninfo"
        self.tender_url = BASE_URL + "/trust/trust/tender"
        self.mytenderlist_url = BASE_URL + "/loan/tender/mytenderlist"
        self.recharge_url = BASE_URL + "/trust/trust/recharge"
        self.mertest_url = "http://mertest.chinapnr.com/muser/publicRequests"

    # 定义获取图片验证码接口，通过return传出
    def get_imgverifycode(self, session, r):
        url = self.img_verify_code_url + r
        return session.get(url)

    # 定义获取短信验证码接口，通过return传出
    def get_phonecode(self, session, phone_data):
        return session.post(self.phone_code_url, data=phone_data)

    # 定义注册接口
    def register(self, session, register_data):
        return session.post(self.register_url, data=register_data)

    # 定义登录接口
    def login(self, session, login_data):
        return session.post(self.login_url, data=login_data)

    # 定义是否登录接口
    def islogin(self, session):
        return session.post(self.islogin_url)

    # 定义认证接口
    def approve(self, session, approve_data):
        return session.post(self.approve_url, data=approve_data)

    # 定义获取认证信息接口
    def get_approve(self, session):
        return session.post(self.get_approve_url)

    # 定义开户接口
    def account(self, session):
        return session.post(self.account_url)

    # 定义第三方接口
    def mertest(self, session, mertest_data):
        return session.post(self.mertest_url, data=mertest_data)

    # 定义充值接口
    def recharge(self, session, recharge_data):
        return session.post(self.recharge_url, data=recharge_data)

    # 定义获取投资产品详情接口
    def loaninfo(self, session, loaninfo_data):
        return session.post(self.loaninfo_url, data=loaninfo_data)

    # 定义投资接口
    def tender(self, session, tender_data):
        return session.post(self.tender_url, data=tender_data)

    # 定义投资列表接口
    def mytenderlist(self, session):
        return session.post(self.mytenderlist_url)
