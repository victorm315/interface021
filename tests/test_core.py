#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020-07-12 11:52
# @Author  : Mingchen.Ma

def test_version():
    """第一个单元测试，校验是不是一个字符串格式"""
    from hogwarts_apitest import __version__
    assert isinstance(__version__, str)