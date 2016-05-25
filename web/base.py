#!/bin/env python3
#coding:utf-8
#公用的模块
import base64
def encode(str):
    encodestr=base64.b64encode(str.encode())
    return encodestr.decode()
def decode(str):
    decodestr=base64.b64decode(str)
    return decodestr.decode()
