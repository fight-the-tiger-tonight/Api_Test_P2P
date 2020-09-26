import json
import logging
import pymysql
import requests
from bs4 import BeautifulSoup

from app import BASE_DIR


def read_imgcode_files():
    file_path = BASE_DIR + "/data/get_imgcode.json"
    register_data = []
    with open(file_path, encoding="utf-8") as f:
        test_case = json.load(f)
        for n in test_case.get("get_imgcode_data"):
            register_data.append((n.get("type"), n.get("status_code")))
    return register_data


def read_register_files():
    file_path = BASE_DIR + "/data/register.json"
    register_data = []
    with open(file_path, encoding="utf-8") as f:
        test_case = json.load(f)
        for n in test_case.get("test_register"):
            register_data.append((n.get("phone"), n.get("pwd"), n.get("verifycode"), n.get("phone_code"),
                                  n.get("dyServer"), n.get("invitephone"), n.get("status_code"), n.get("status"),
                                  n.get("description")))
    return register_data


# 统一读取所有的参数数据文件代码
def read_param_data(file_name, method_name, param_names):
    """
    :param file_name:
    :param method_name:
    :param param_names:
    :return:
    """
    data_file = BASE_DIR + "/data/" + file_name
    test_case_data = []
    with open(data_file, encoding="utf-8") as f:
        dict_data = json.load(f)
        for test_data in dict_data.get(method_name):
            # 定义一组列表，存放一组est_data中所有的测试数据
            test_params = []
            for param in param_names.split(','):
                # 依次读取每一个参数的值，添加到test_params中，形成一个列表
                test_params.append(test_data.get(param))
            test_case_data.append(test_params)
        print("test_case_data = {}".format(test_case_data))
    return test_case_data


# 封装公用断言方法
def assert_utils(self, response, status_code, status, description):
    self.assertEqual(status_code, response.status_code)
    self.assertEqual(status, response.json().get("status"))
    self.assertEqual(description, response.json().get("description"))


# 封装公用发送第三方接口请求
def third_request_api(form_data):
    # 解析form表达那中的内容，并提取参数发送第三方请求
    soup = BeautifulSoup(form_data, 'html.parser')
    third_requests_url = soup.form['action']
    data = {}
    for input in soup.find_all('input'):
        data.setdefault(input['name'], input['value'])
    logging.info("third requests data={}".format(data))
    response = requests.post(third_requests_url, data=data)
    logging.info("third response = {}".format(response.text))
    return response


def connet_mysql(sql):
    # 创建连接
    connet = pymysql.connect(host="52.83.144.39", port=3306, user="root", password="Itcast_p2p_20191228",
                             database="czbk_member")
    # 创建游标
    cursor = connet.cursor()
    # 执行sql
    cursor.execute(sql)
    print(cursor.fetchall())
    # 关闭游标
    cursor.close()
    # 关闭连接
    connet.close()


class DBUtils:
    @classmethod
    def get_connet(cls):
        conn = pymysql.connect(host="52.83.144.39", port=3306, user="root", password="Itcast_p2p_20191228",
                               database="czbk_member")
        return conn

    @classmethod
    def close_conn(cls, cursor, conn):
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    @classmethod
    def execute_sql(cls, sql):
        try:
            conn = cls.get_connet()
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()
        finally:
            cls.close_conn(cursor, conn)
