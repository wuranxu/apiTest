__author__ = 'Woody'
'''存放功能函数的类
'''
import inspect
import json
from initial import app
import os


class Operator(object):

    def __init__(self):
        pass

    @classmethod
    def get_current_func(self):
        '''
        :return: 返回当前函数名
        '''
        return inspect.stack()[1][3]

    @classmethod
    def getFileList(self):
        file_list = []
        workspace = app.config['WORKSPACE']
        for root, dirs, files in os.walk(workspace):
            if app.config['CONFIG_XLSX'] in files:
                files.remove(app.config['CONFIG_XLSX'])
            for f in files:
                file_list.append(os.path.join(root, f))
        return file_list

    @classmethod
    def transfer_str(self, **kwargs):
        rt = {}
        for key in kwargs:
            value = kwargs.get(key)
            try:
                value = json.loads(value)
            except:
                pass
            rt.update({key: value})
        return rt


    @classmethod
    def transfer_case_info(self, case):
        for key, value in case.items():
            if isinstance(value, dict) or isinstance(value, list):
                case.update({key: dumps(value)})
        return case












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
