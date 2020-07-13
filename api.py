#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-07-12 22:22
# @Author  : Mingchen.Ma

# 第一部分：针对单个api的框架封装
import requests

class BaseApi(object):
    method = "GET"
    url = ""
    parmas = {}
    headers = {}
    cookies = {}
    data = {}
    json = {}
    
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
        self.response = requests.request(
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
        return self