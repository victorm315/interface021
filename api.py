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
        actual_result = getattr(self.response, key)
        assert actual_result == expected_value
        return self