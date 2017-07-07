__author__ = 'Woody'
from initial import app
from common.function import Operator, json
from common.excelReader import reader
import logging
import requests
from common.function import dumps
from db_operator.mysql_db import MysqlDb


class run(object):

    def get_api_status(self):
        filepath = app.config.get('LOG_CONFIG')
        book = reader(filepath)
        return list(book.get_addr_status())

    def run_case(self, case_list, threadName, result):
        '''

        :param case_list:
        :return: 包含case信息和case状态的列表
        '''
        # 获取成功case的数量
        success_num, fail_num = 0, 0
        rt = {}
        success, failure, passed = [], [], []
        closed = self.get_api_status()
        for case in case_list:
            # 判断case是否运行
            if case.get('url') not in closed:
                # 说明有前置条件
                precondition = False if case.get('precondition') == '' else True
                # 如果有前置条件，转换数据之后处理完所有前置条件
                if precondition:
                    new_pre = []
                    for x in case.get('pre'):
                        new_pre.append(self.transfer_data(x))
                    case.update(dict(pre=new_pre))
                case = self.transfer_data(case)
                # 如果case打开
                if case.get('enable'):
                    if precondition:
                        pres = case.get('pre')
                        for pre in pres:
                            self.request(**pre)
                    # 数据库准备
                    sql = case.get('sql_prepare')
                    # 数据库校验
                    sql_verify = case.get('sql_verify')
                    # 数据库清理
                    sql_clean = case.get('sql_clean')

                    self.prepare(sql, case)
                    rv = self.request(**case)
                    self.verify(sql_verify, rv)
                    self.clean(sql_clean)
                    # 获取用例执行状态，如果为失败则添加到失败列表
                    if rv.get('status'):
                        success.append(rv)
                        success_num += 1
                    else:
                        failure.append(rv)
                        fail_num += 1
                else:
                    passed.append({'caseInfo': case})
            else:
                passed.append({'caseInfo': case})
        rt.update(dict(success=success, fail=failure, not_run=passed, ignored=len(passed),
                       success_num=success_num, failed_num=fail_num, total=fail_num+success_num+len(passed),
                       ))
        result.update(dict({threadName: rt}))

    def prepare(self, sql, case):
        if sql:
            obj = MysqlDb(app.config['DBNAME'])
            value = getattr(obj, sql)()
            pre_data = case.get('pre_data')
            params = json.loads(case.get('params'))
            requestData = params.get('requestData')
            requestData.update({pre_data: value})
            params.update(dict(requestData=requestData))
            case.update(dict(params=dumps(params)))
            del obj

    def verify(self, sql_verify, rv):
        if sql_verify:
            obj = MysqlDb(app.config['DBNAME'])
            verify = getattr(obj, sql_verify)()
            if not verify:
                rv.update(dict(status=False, msg="数据库校验不正确!请检查!"))
            del obj

    def clean(self, sql_clean):
        if sql_clean:
            obj = MysqlDb(app.config['DBNAME'])
            getattr(obj, sql_clean)()
            del obj

    def data_to_json(self, string):
        '''

        :param string:
        :return: json数据转为dict
        '''
        if isinstance(string, str):
            string = string.replace("'", '"').replace("\n", '')
            return json.loads(string)
        else:
            return string

    def form_to_dict(self, string):
        '''

        :param string:
        :return: form数据转为dict
        '''
        d = {}
        params = string.split('&')
        for data in params:
            key, value = data.split('=')
            d.update({key: value})
        return d

    def get_response(self, text):
        '''

        :param text:
        :return: 如请求结果能转为dict对象，则转化，不能则返回请求结果
        '''
        try:
            return json.loads(text)
        except:
            return text

    def transfer_data(self, case):
        try:
            params = self.addToken(case.get('params'))
            enable = case.get('enable')
            code = int(case.get('code'))
            headers = case.get('headers')
            expected = self.get_response(case.get('expected'))
            if params != '' and isinstance(params, str):
                params = self.form_to_dict(params) if 'form' in headers else dumps(self.data_to_json(params))
            else:
                params = dumps(params)
            headers = self.data_to_json(headers)
            case.update(dict(headers=headers, params=params,
                             enable=enable, code=code,
                             expected=expected))
        except Exception as err:
            logging.error("{} error: {}".format(Operator.get_current_func(), str(err)))
        return case

    def addToken(self, params):
        try:
            params = json.loads(params)
            params.update(dict(token=app.config['TOKEN']))
            params = dumps(params)
        except:
            pass
        return params

    def pretty_data(self, case):
        try:
            if not isinstance(case.get('params'), str):
                params = dumps(case.get('params'))
            else:
                params = case.get('params')
            headers = dumps(case.get('headers'))
            expected = dumps(case.get('expected'))
            actually = dumps(case.get('actually'))
            case.update(dict(headers=headers, params=params, expected=expected, actually=actually))
        except Exception as err:
            logging.error("{} error: {}".format(Operator.get_current_func(), str(err)))

    def request(self, **kwargs):
        '''

        :param kwargs:
        :return: 单个case运行结果
        '''
        rt = {'status': False, 'msg': '', 'caseInfo': kwargs}
        try:
            # 获取用例的参数如url, expected
            method = kwargs.get('method', 'GET')
            url = kwargs.get('url')
            expected = kwargs.get('expected')
            headers = kwargs.get('headers')
            params = kwargs.get('params')
            code = kwargs.get('code')
            _assert = kwargs.get('_assert')
            # 获取超时配置
            timeout = app.config['TIMEOUT']
            # 更新解析后的params和headers信息
            kwargs.update(dict(params=params, headers=headers))
            # 判断请求方法是post还是get
            if method.lower() == 'post':
                r = requests.post(url=url, data=params, timeout=timeout, headers=headers)
            else:
                r = requests.get(url=url, headers=headers, timeout=timeout)
            # 解析返回数据
            data = self.get_response(r.text)
            kwargs.update(dict(actually=data))
            self.pretty_data(kwargs)
            rt.update({'caseInfo': kwargs})
            # 判断返回状态码和预期状态码是否一致
            if r.status_code == code:
                kwargs.update(dict(timeout=timeout, rt_code=r.status_code))
                # 对返回结果作断言处理
                self.assertValue(_assert=_assert, expected=expected, actually=data)
                # 如与预期一致则将status置为True
                rt.update(dict(status=True))
            else:
                # 不一致则记录
                kwargs.update(dict(rt_code=r.status_code, msg="http_code 不为 {}".format(code)))
        except Exception as err:
            rt.update(dict(msg=str(err)))
            print(str(err))
            logging.error("{} error: {}".format(Operator.get_current_func(), str(err)))
        return rt

    def assertValue(self, **kwargs):
        # 获取断言需要的3个元素: 断言方式, 预期结果, 实际结果
        _assert = kwargs.get('_assert')
        expected = kwargs.get('expected')
        actually = kwargs.get('actually')
        if _assert.lower() == 'in':
            if isinstance(actually, list):
                assert expected in actually, "返回数据没有包含预期数据"
            elif isinstance(actually, dict):
                for key, value in expected.items():
                    assert value == actually.get(key), "返回数据{}没有包含预期数据{}".format(actually, expected)
            elif isinstance(actually, str):
                assert expected in actually, "返回数据没有包含预期数据"
        elif _assert.lower() == 'equal':
            assert expected == actually, "返回数据与预期数据不相等"
        elif _assert.lower() == 'not equal':
            assert expected != actually, "返回数据与预期数据相等"
        elif _assert.lower() == 'none':
            assert actually is None, "返回数据不为None"
        elif _assert.lower() == 'not none':
            if isinstance(actually, dict):
                for key, value in actually.items():
                    assert value is None, "返回数据{}字段为None".format(key)
            assert actually is not None, "返回数据为None"
        else:
            pass
