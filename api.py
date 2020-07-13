#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-07-12 22:22
# @Author  : Mingchen.Ma

# 第一部分：针对单个api的框架封装
import requests

session = requests.sessions.Session()

class BaseApi(object):
    method = "GET"
    url = ""
    parmas = {}
    headers = {}
    cookies = {}
    data = {}
    json = {}
    
    def __init__(self):
        self.response = None
    
    # 共性的 set_parmas 和  validate 是相同的，尅抽象出来
    def set_parmas(self, **parmas):
        self.parmas = parmas
        return self
    
    def set_data(self, data):
        self.data = data
        return self
    
    def set_json(self, json_data):
        self.json = json_data
        return self
    
    def set_cookie(self, key, value):
        self.cookies.update({key: value})
        return self
    
    # requests所有的方法都是基于request.request()来实现的
    def run(self):
        
        """
        因为run调用的是 requests.request,到 request里其实其实每次调用都会关闭session，导致每次接口调用都会新建一个session，因此cookie也无法带入
        解决方法：
        改写requests.request  等价于 requests.sessions.Session().request,所以可以改写为：
        session = requests.sessions.Session() ,并且可以单独抽离出去放在类外面，值实例化一次
        通过这种方式就可以将各个接口间进行公用
        """
        
        self.response = session.request(
            method=self.method,
            url=self.url,
            params=self.parmas,
            headers=self.headers,
            cookies = self.cookies,
            data=self.data,
            json=self.json
        )
        return self
    

    
    def extract(self, field):
        """提取响应中的数据"""
        """这里要先做好约定，extract后能否更validate
            当前约定：不可以，extract只能在最后,所以就直接return的是提取出来的值，而不是return self
            
        """
        # todo: 对run之后可以提取，提取后可以validate提取的是否正确，问题是是否有必要这么做

        value = self.response
        for _key in field.split("."):
            if isinstance(value, requests.Response):
                if _key in ["json()", "json"]:
                    value = self.response.json()
                else:
                    value = getattr(value, _key)
            elif isinstance(value, (requests.structures.CaseInsensitiveDict, dict)):
                value = value[_key]
        
        # 提取响应中的状态码
        return value
    
    def validate(self, key, expected_value):
        """key是要传入的待断言字段"""
        
        """由于在extract里也同样要用到下面的代码，因为都是从response里提取数据，
        公共部分代码，抽离出来，单独放到extract里去"""
        # value = self.response
        # for _key in key.split("."):
        #     print("value----", _key, value,type(value),expected_value)
        #     print("json======", _key, value)
        #     if isinstance(value, requests.Response):
        #         if _key in ["json()", "json"]:
        #             value = self.response.json()
        #         else:
        #             value = getattr(value, _key)
        #     elif isinstance(value, (requests.structures.CaseInsensitiveDict,dict)):
        #         value = value[_key]
        # todo : 校验异常未捕获，一旦某个校验失败，就会终止其他校验。改成可以继续执行
        actual_value = self.extract(key)
        assert actual_value == expected_value
        # self 返回的是类实例，其实就是BaseApi
        return self
    
    
    def get_response(self):
        """因为只有run里才会有response，所以需要先在__init__里要初始化self.response = None
        当run运行后，有值，就可以返回了"""
        return self.response