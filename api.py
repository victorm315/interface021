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
    
    # requests所有的方法都是基于request.request()来实现的
    def run(self):
        self.response = requests.request(
            method=self.method,
            url=self.url,
            params=self.parmas,
            headers=self.headers,
            data=self.data,
            json=self.json
        )
        return self
    
    def validate(self, key, expected_value):
        """key是要传入的待断言字段"""
        value = self.response
        for _key in key.split("."):
            print("value----", _key, value,type(value),expected_value)
            print("json======", _key, value)
            if isinstance(value, requests.Response):
                if _key in ["json()", "json"]:
                    value = self.response.json()
                else:
                    value = getattr(value, _key)
            elif isinstance(value, (requests.structures.CaseInsensitiveDict,dict)):
                value = value[_key]
        # todo : 校验异常未捕获，一旦某个校验失败，就会终止其他校验。改成可以继续执行
        assert value == expected_value
        return self