#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2016-04-17 16:29:45
# @Author  : NvRay (nvray@foxmail.com)

from db import dbconn

class BuitInAttrError(Exception):
    """BuitIn Attri Error"""


class Field(dict):

    """Container of field metadata"""


class meta(type):

    def __setitem__(self, key, value):
        if key in dir(self):
            type.__setattr__(self, key, value)
        elif key[0] == "_":
            raise BuitInAttrError
        else:
            raise AttributeError

    def __getitem__(self, key):
        if key[0] == "_":
            raise BuitInAttrError
        return type.__getattribute__(self, key)


class SinaWeiboItem(object):
    __metaclass__ = meta
    
    name = Field()
    uid = Field()
    info = Field()
