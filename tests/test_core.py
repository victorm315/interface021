#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-07-12 11:52
# @Author  : Mingchen.Ma
from api import BaseApi
from tests.api import ApiHttpbinGet, ApiHttpBinPost, ApiHttpbinGetCookies, ApiHttpBinGetSetCookies


def test_version():
    """第一个单元测试，校验是不是一个字符串格式"""
    from hogwarts_apitest import __version__
    assert isinstance(__version__, str)
    
# import requests
#
# class BaseApi(object):
#
#     method = "GET"
#     url = ""
#     parmas = {}
#     headers = {}
#     data = {}
#     json = {}
#
#     # 共性的 set_parmas 和  validate 是相同的，尅抽象出来
#     def set_parmas(self, **parmas):
#         self.parmas = parmas
#         return self
#
#     def set_data(self, data):
#         self.data = data
#         return self
#
#     def set_json(self, json_data):
#         self.json = json_data
#         return self
#
#     # requests所有的方法都是基于request.request()来实现的
#     def run(self):
#         self.response = requests.request(
#             method = self.method,
#             url = self.url,
#             params = self.parmas,
#             headers = self.headers,
#             data = self.data,
#             json = self.json
#         )
#         return self
#
#     def validate(self, key, expected_value):
#         actual_result = getattr(self.response, key)
#         assert actual_result == expected_value
#         return self


# class ApiHttpbinGet(BaseApi):
    """对测试接口的定义"""
#     url = "http://httpbin.org/get"
#     parmas = {}
#     method = "get"
#     headers = {"accept": "application/json"}
    
    # def set_parmas(self, **parmas):
    #     self.parmas = parmas
    #     return self
    
    # def run(self):
    #     self.response = requests.get(
    #         self.url,
    #         params = self.parmas,
    #         headers = self.headers
    #     )
    #     return self
    
    # 为了统一，使用requests.request
    # def run(self):
    #     self.response = requests.request(
    #         self.method,
    #         self.url,
    #         params = self.parmas,
    #         headers = self.headers,
    #         data = self.data,
    #         json = self.json
    #     )
    #     return self
    
    # def validate(self,key, expected_value):
    #     actual_result = getattr(self.response, key)
    #     assert actual_result == expected_value
    #     return self

# class ApiHttpBinPost(BaseApi):
#     url = "http://httpbin.org/post"
#     method = "post"
#     parmas = {}
#     headers = {"accept": "application/json"}
#     data = "abc=123"
#     json = {"xyz": 123}
    

    
    # def run(self):
    #     self.response = requests.request(
    #         self.method,
    #         self.url,
    #         params = self.parmas,
    #         headers = self.headers,
    #         data = self.data,
    #         json = self.json
    #     )
    #     return self

    
    # def validate(self,key, expected_value):
    #     actual_result = getattr(self.response, key)
    #     assert actual_result == expected_value
    #     return self

# 每个函数对应一个测试用例

def test_httpbin_get():
    # 1 .构造参数
    # 2. 发送请求
    # resp = requests.get(
    #     "http://httpbin.org/get",
    #     headers = {"accept": "application/json"}
    # )
    # # 3. 断言
    # assert resp.status_code == 200
    # assert resp.headers["server"] == "gunicorn/19.9.0"
    # assert resp.json()["url"] == "http://httpbin.org/get"
    
    ApiHttpbinGet().run()\
        .validate("status_code", 200)\
        .validate("headers.server","gunicorn/19.9.0")\
        .validate("json().url", "http://httpbin.org/get")\
        .validate("json().args", {})\
        .validate("json().headers.Accept", "application/json")\
        .validate("json.url", "http://httpbin.org/get")
        # 注意：因为response要转化为json格式，应该是resp.json()，但是目前validate里的
        # 写法是 json.url,肯定是获取不到的
        # 前期为了快速实现，就先改为json().url, todo：后期需要改成 json.url的
    
    
    
def test_httpbin_get_with_parmas():
    # resp = requests.get(
    #     "http://httpbin.org/get",
    #     params= {"abc":123},
    #     headers = {"accept": "application/json"}
    # )
    # assert resp.status_code == 200
    # assert resp.headers["server"] == "gunicorn/19.9.0"
    # assert resp.json()["url"] == "http://httpbin.org/get?abc=123"
    
    # parmas = {"abc":123, "xyz":456}
    
    ApiHttpbinGet()\
        .set_parmas(abc=123,xyz=456) \
        .run() \
        .validate("status_code", 200)\
        .validate("json.url", "http://httpbin.org/get?abc=123&xyz=456") \
        .validate("json().headers.Accept", "application/json")
        # parmas还可以以这种方式传，这样的话-> set_parmas(self,parmas)
        # .set_parmas(parmas)\


def test_httpbin_post():
    # resp = requests.post(
    #     "http://httpbin.org/post",
    #     headers = {"accept": "application/json"},
    #     json={"abc":"1234"}
    #     # data={"abc":"1234"}
    # )
    # print("resp.json====", resp.json())
    # assert resp.status_code == 200
    # assert resp.headers["server"] == "gunicorn/19.9.0"
    # assert resp.json()["url"] == "http://httpbin.org/post"
    # assert resp.json()["json"]["abc"] == "1234"
    # # assert resp.json()["form"]["abc"] == "1234"
    
    ApiHttpBinPost()\
        .set_json({"xyz": 456})\
        .run()\
        .validate("status_code", 200)\
        .validate("headers.server", 'gunicorn/19.9.0')\
        .validate("json().headers.Accept", "application/json")\
        .validate("json.url", "http://httpbin.org/post")\


# 用户故事2 参数关联
# test_httpbin_paraments_share是个测试用例
def test_httpbin_paraments_share():
    """实现参数共享,多个接口里都会用到user_id
        美观度不好，但是已经实现了测试步骤一和测试步骤2实现参数共享的机制
        可以在通过迭代来美观和提高灵活性
    """
    user_id = "adk129"
    # 测试步骤1：get请求，获取某些信息
    ApiHttpbinGet() \
        .set_parmas(user_id=user_id) \
        .run() \
        .validate("status_code", 200) \
        .validate("json.url", "http://httpbin.org/get?user_id={}".format(user_id)) \
        .validate("json().headers.Accept", "application/json")

    # 测试步骤2：post请求，提交数据
    ApiHttpBinPost() \
        .set_json({"user_id": user_id}) \
        .run() \
        .validate("status_code", 200) \
        .validate("headers.server", 'gunicorn/19.9.0') \
        .validate("json().headers.Accept", "application/json") \
        .validate("json.url", "http://httpbin.org/post")\
        .validate("json().json.user_id", "adk129")
    
# 用户故事2

def test_httpbin_extract():
    """测试提取响应值里的状态码"""
    
    # status_code = ApiHttpbinGet() \
    #     .run() \
    #     .extract("status_code")
    # assert status_code == 200
    #
    # """测试提取headers里的Server"""
    # server = ApiHttpbinGet().run().extract("headers.server")
    # assert server == "gunicorn/19.9.0"
    #
    # accept_type = ApiHttpbinGet().run().extract("json().headers.Accept")
    # assert accept_type == "application/json"
    
    # 上面是从一个接口里提取了三个数据，但是接口却被请求了三次，这是不合理的
    # 下面通过请求一次接口，然后提取数据实现
    
    api_run = ApiHttpbinGet().run()
    
    status_code = api_run.extract("status_code")
    assert status_code == 200

    """测试提取headers里的Server"""
    server = api_run.extract("headers.server")
    assert server == "gunicorn/19.9.0"

    accept_type = api_run.extract("json().headers.Accept")
    assert accept_type == "application/json"
    
    
def test_httpbin_setcookies():
    """测试set cookie"""
    api_run = ApiHttpbinGetCookies()\
        .set_cookie("freeform1", "123")\
        .set_cookie("freeform2", "456")\
        .run()
    
    freeform1 = api_run.extract("json().cookies.freeform1")
    freeform2 = api_run.extract("json().cookies.freeform2")
    
    assert freeform1 == "123"
    assert freeform2 == "456"
    
def test_httpbin_paraments_extract():
    """实现测试步骤之间的参数依赖
    """
    # 测试步骤1：get请求，获取cookie,并提取
    freeform = ApiHttpbinGetCookies()\
        .set_cookie("freeform", "123")\
        .run()\
        .extract("json.cookies.freeform")
    
    assert freeform == "123"

    # 测试步骤2：post请求，提交数据，并把测试步骤1里提取的数据作为参数使用
    ApiHttpBinPost() \
        .set_json({"freeform": freeform}) \
        .run() \
        .validate("status_code", 200) \
        .validate("headers.server", 'gunicorn/19.9.0') \
        .validate("json().headers.Accept", "application/json") \
        .validate("json.url", "http://httpbin.org/post")\
        .validate("json().json.freeform", freeform)
    

def test_httpbin_login_status():
    # Step1: 类似 login and get cookie 的功能
    ApiHttpBinGetSetCookies().set_parmas(freeform="567").run()

    # Step2: Post 请求，不用再单独设置cookie，就能用Step1返回的cookie, 并且请求的header里携带着上面的cookies
    resp = ApiHttpBinPost()\
        .set_json({"abc":"123"})\
        .run()\
        .get_response()
    # 这里获取的
    request_headers = resp.request.headers
    assert "freeform=567" in request_headers["Cookie"]
