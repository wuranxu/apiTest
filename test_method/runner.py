__author__ = 'Woody'
from initial import app
from common.function import Operator, json
from common.excelReader import reader
import logging
import requests
from datetime import datetime
from common.function import dumps

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
        start = datetime.now().strftime(app.config['TIMEFORMAT'])
        success_num, fail_num = 0, 0
        rt = {}
        success, failure, passed = [], [], []
        closed = self.get_api_status()
        for case in case_list:
            # 判断case是否运行
            if case.get('url') not in closed:
                case = self.transfer_data(case)
                if case.get('enable'):
                    rv = self.request(**case)
                    if rv.get('status'):
                        success.append(rv)
                        success_num += 1
                    else:
                        failure.append(rv)
                        fail_num += 1
                else:
                    passed.append({'caseInfo': case})
            # self.pretty_data(case)
        end = datetime.now().strftime(app.config['TIMEFORMAT'])
        pluse = (datetime.now() - datetime.strptime(start, app.config['TIMEFORMAT'])).total_seconds()
        rt.update(dict(success=success, fail=failure, not_run=passed, ignored=len(passed),
                       success_num=success_num, failed_num=fail_num, total=fail_num+success_num+len(passed),
                       start=start, end=end, cost=pluse
                       ))
        result.update(dict({threadName: rt}))

    def data_to_json(self, string):
        '''

        :param string:
        :return: json数据转为dict
        '''
        string = string.replace("'", '"').replace("\n", '')
        return json.loads(string)

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
            params = case.get('params')
            enable = case.get('enable')
            code = int(case.get('code'))
            headers = case.get('headers')
            expected = self.get_response(case.get('expected'))
            params = self.form_to_dict(params) if 'form' in headers else json.dumps(self.data_to_json(params), indent=1)
            headers = self.data_to_json(headers)
            case.update(dict(headers=headers, params=params, enable=enable, code=code, expected=expected))
        except Exception as err:
            logging.error("{} error: {}".format(Operator.get_current_func(), str(err)))
        return case

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
                    assert value == actually.get(key), "返回数据没有包含预期数据"
            elif isinstance(actually, str):
                assert expected in actually, "返回数据没有包含预期数据"
        elif _assert.lower() == 'equal':
            assert expected == actually, "返回数据与预期数据不相等"
        elif _assert.lower() == 'not equal':
            assert expected != actually, "返回数据与预期数据相等"
        elif _assert.lower() == 'none':
            assert expected is None, "返回数据不为None"
        elif _assert.lower() == 'not none':
            assert expected is not None, "返回数据为None"
        else:
            pass
