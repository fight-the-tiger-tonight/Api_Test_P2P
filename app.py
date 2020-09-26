import logging.handlers
import os
import time

BASE_URL = "http://user-p2p-test.itheima.net"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHONE1 = "18212345670"
PHONE2 = "18212345671"
PHONE3 = "18212345672"
PHONE4 = "18212345673"
PHONE5 = "18212345674"
PHONE6 = "18212345675"
PHONE_x = "18212345676"


# 初始化日志配置
def log_config():
    # 初始化日志对象
    loger = logging.getLogger()
    # 设置日志级别
    loger.setLevel(logging.INFO)
    # 创建控制台日志处理器和文件日志处理器
    # log_file = './log/P2P.log'
    log_file = BASE_DIR + os.sep + 'log' + os.sep + 'P2P-{}.log'.format(time.strftime("%Y%m%d-%H.%M.%S"))
    sh = logging.StreamHandler()
    fh = logging.handlers.TimedRotatingFileHandler(log_file, when='M', interval=3, backupCount=3, encoding='utf-8')
    # 设置日志格式，创建格式化器
    fmt = '%(asctime)s %(levelname)s [%(name)s] [%(filename)s(%(funcName)s:%(lineno)d)] - %(message)s'
    formatter = logging.Formatter(fmt)
    # 将格式化器设置到日志器中
    sh.setFormatter(formatter)
    fh.setFormatter(formatter)
    # 日志器添加到日志对象
    loger.addHandler(sh)
    loger.addHandler(fh)
