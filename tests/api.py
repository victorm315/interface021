#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-07-13 06:34
# @Author  : Mingchen.Ma

# 对接口的定义

# TODO 可以利用抓包工具，动态生成这些接口，实现与yaml文件的动态隐射，抓包生成，probuffer
#

from api import BaseApi

class ApiHttpbinGet(BaseApi):
    url = "http://httpbin.org/get"
    parmas = {}
    method = "get"
    headers = {"accept": "application/json"}

class ApiHttpBinPost(BaseApi):
    url = "http://httpbin.org/post"
    method = "post"
    parmas = {}
    headers = {"accept": "application/json"}
    data = "abc=123"
    json = {"xyz": 123}