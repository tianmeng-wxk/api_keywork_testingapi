import requests
from common import read_yaml, connect_mysql, log

data = read_yaml('./config/url.yaml')
class Httpclien():

    INDEX = 0
    def __init__(self):
        self.log = log()
        self.init_url_headers()
        #self.sql = connect_mysql()


    def init_url_headers(self):
        self.url = data["test_environment"]["url"]
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}

    def get_sql_data(self,sql):
        sql = connect_mysql(sql)
        return sql

    def get(self,data):
        try:
            r = requests.get(url=self.url,params=data,headers=self.headers)
            return r.json()
        except BaseException as e:
            raise ("接口发生未知错误", e)

    def post(self,data,files):
        try:
            r = requests.post(url=self.url,data=data,headers=self.headers,files=files)
            return r.json()

        except BaseException as e:
            raise ("接口发生未知错误", e)

    def detelet(self,data):
        try:
            r = requests.post(url=self.url, data=data, headers=self.headers)
            return r.json()
        except BaseException as e:
            print("接口发生未知错误", e)

    def send_request(self, methon, name=None, data=None, files=None,headers=None):
        Httpclien.INDEX+=1

        self.log.info("发送第{1}个请求 url:{0} params:{2}".format(self.url+name, Httpclien.INDEX, data))

        #从extract.yaml文件获取token添加到headers
        if headers:
            for key,value in headers.items():
                if value.startswith("${{") and value.endswith("}}"):
                    value=value.split("{{")[1].split("}}")[0]
                    from common import read_yaml_extract
                    value=read_yaml_extract(value)
                    self.log.info("获取到的token:{}".format(value))

                self.headers[key]=value

            self.log.info("headers：{}".format(self.headers))
        # if data:
        #     if isinstance(data,dict):
        #         import json
        #         data = json.dumps(data)#字典才转换成json字符串
        #     #return data
        # print("data是：",data)

        self.url = self.url+name

        methon = methon.upper()
        res = ''
        if methon == "GET":
            res = self.get(data)
        elif methon == "POST":
            res = self.post(data,files)
        elif methon == "DETELET":
            res = self.detelet(data)
        #self.init_url_headers()
        return res






