import unittest,pytest,os,sys
from key_work import Httpclien
from ddt import ddt, file_data,unpack
from common import log
# from read_yaml import read_yaml
# data = read_yaml()
import os
current_path = os.path.abspath(os.path.dirname(__file__))
@ddt
class Test_api(unittest.TestCase):
    # url = data["login"]["url"]
    #session = requests.session()
    token = ''

    def setUp(self) -> None:
        self.clien = Httpclien()
        self.log = log()
    def tearDown(self) -> None:
        pass

    # 验证结果hans
    def validate(self,expect,actual):
        for key,value in expect.items():
            if key in actual:
                self.assertEqual(value,actual[key])
            else:
                for _key,_value in actual.items():
                    if isinstance(_value,dict) and (key in _value):
                        #self.assertEqual(value,_value[key])
                        expect_new={}
                        expect_new[key]=value
                        #使用递归函数
                        self.validate(expect_new,_value)

#获取token的请求
    # def test_auth(self):
    #     # response = self.session.post(self.url+"auth")
    #     # jsonres = json.loads(response.text)
    #     # print(jsonres)
    #     # self.session.headers["token"] = jsonres["token"]#之后的每个用例不必在headers同步token
    #     # self.assertEqual(jsonres["status"], 200, msg="获取token失败")
    #     res = self.clien.send_request("post", name="auth")
    #     Test_api.token = res["token"]
    #     print("response：",res)
# #登录
#     @file_data(current_path+"../../config/login.yaml")
#     @unpack
#     def test_login(self,**data):
#         # data = kwargs["request"].get("params")
#         # validata = kwargs["validata"].get("msg")
#         #print("token为:{}".format(Test_api.token))
#         #data = {"username": "Will", "password": 123456}
#         headers = {
#             "token": Test_api.token
#         }
#         # response = self.session.post(self.url+"login", data=data)
#         # res = response.json()
#     #   print(res)
#     #   self.assertEqual(res["msg"], "恭喜您，登录成功", msg="登录失败")
#         res = self.clien.send_request(data["request"]["methon"], name=data["apiname"], data=data["request"]["params"],  headers=headers)
#         print(res)
#         self.validate(data["validata"], res)
#         print("1111111111111111111")
#         #logout("111", headers=headers)
#
#
#
#
# #登出
#     def test_logout(self):
#         headers = {
#             "token": Test_api.token
#         }
#         # print(self.session.headers["token"])
#         # response = self.session.post(self.url+"logout")
#         # res = response.json()
#         # print(res)
#         # res = self.assertEqual(res["msg"], "用户已退出登录", msg="登出失败")
#         res = self.clien.send_request("post", name="logout",headers=headers)
#         self.assertEqual(res["msg"], "用户已退出登录", msg="登出失败")
#         print("response：", res)
#         # res  = self.clien.send_request(data["request"]["methon"],name=data["apiname"],headers=headers)
#         # self.validate(data["validata"],res)


    #运行用例汇总
    @file_data("./config/login.yaml")
    @unpack
    def test_interface(self,**data):

        # headers = {
        #     "token": Test_api.token
        # }
        res = self.clien.send_request(data["request"]["methon"], name=data["apiname"], data=data["request"]["params"],headers=data["request"]["headers"])

        self.log.info("返回的数据：{}".format(res))
        #验证yaml中的验证字段
        if 'extract' in data and data['extract']:
            for key,value in data['extract'].items():
                extract={}
                extract[key]=res[value]
                from common import write_yaml
                write_yaml(extract)
                self.log.info("yaml文件保存更新的token内容：{}".format(extract))
        #验证结果
        self.validate(data["validata"], res)


if __name__ == '__main__':
    #unittest.main()
    pytest.main(["-s", "./testcase.py", "--html=./config/report/py_report.html"])
    #"--maxfail=1"出现一次失败就终止测试
    # ,"-n=2"多cpu分发运行#pytest-xdist
    #--reruns number pytest-rerunfailures重复运行失败用例




