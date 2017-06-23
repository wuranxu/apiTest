__author__ = 'Woody'
'''存放功能函数的类
'''
import inspect
import json


class Operator(object):

    def __init__(self):
        pass

    @classmethod
    def get_current_func(self):
        '''
        :return: 返回当前函数名
        '''
        return inspect.stack()[1][3]



def dumps(obj):
    '''

    :param obj:
    :return: json解析后的字符串
    '''
    return json.dumps(obj, ensure_ascii=False, indent=1)


def loads(text):
    '''

    :param text:
    :return: Python内置对象dict
    '''
    return json.loads(text)