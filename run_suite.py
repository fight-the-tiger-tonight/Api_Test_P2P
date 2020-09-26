import time
import unittest
from app import BASE_DIR
from lib.HTMLTestRunner import HTMLTestRunner

# suite = unittest.TestSuite()
# suite.addTest(unittest.makeSuite(TestTender))
suite = unittest.defaultTestLoader.discover("./script", "P2P*")
# 指定报告路径/
report = BASE_DIR + "/report/report-{}.html".format(time.strftime("%Y%m%d-%H%M%S"))
# 打开文件
with open(report, 'wb') as f:
    # runner = HTMLTestRunnerCN
    runner = HTMLTestRunner(f, title='P2P金融项目接口自动化测试报告',description="测试环境：python 3.6.4")
    runner.run(suite)
