__author__ = 'Woody'
import os
from threading import Thread

from flask import render_template

from common.excelReader import reader
from common.time_handle import handle
from initial import app
from test_method.runner import run

result = {}

class apiFunc(object):

    def writeReport(self, rt):
        # 写入结果到测试报告
        filename = handle.now().strftime("%Y-%m-%d %H-%M-%S") + ".html"
        htmlPath = os.path.join(app.config['REPORT'], filename)
        # 写入测试报告到本地html文件
        with open(htmlPath, mode='w+', encoding='utf-8') as f:
            f.write(render_template('testReport.html', successful=rt['success'],
                               failed=rt['fail']))
        return filename

    def run_test(self, dir, filename, threadNum):
        global result
        # 读取reader类的实例
        rd = reader(filepath=os.path.join(dir, filename))
        rt = self.multiple_run(rd, threadNum)
        # 释放excel文件
        rd.release_source()
        return rt

    def divide_case(self, *args):
        case_num, num = args
        return int(case_num / num) if (case_num % num) == 0 else int(case_num / num) + 1

    def multiple_run(self, rd, threadNum):
        # 获取filename里接口用例列表
        case_list = rd.get_case_list()
        # 拆分用例
        divide = self.divide_case(len(case_list), threadNum)
        total_case = [case_list[i:i+divide] for i in range(0, len(case_list), divide)]
        # 生成Operator类实例
        obj = run()
        # 运行case_list里边的case
        threads = []
        for i in range(len(total_case)):
            threads.append(Thread(target=obj.run_case, args=(total_case[i], "thread_{}".format(i), result)))
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        return self.deal_with_result(result)

    def deal_with_result(self, result):
        rt = {}
        # 整合报告
        for value in result.values():
            for k, v in value.items():
                # 如果结果里存在了则添加，不存在则插入
                if rt.get(k):
                    if isinstance(v, list) and v:
                        rt[k].extend(v)
                        # 排序
                        rt[k] = sorted(rt[k], key=lambda x: x['caseInfo']['name'])
                    elif isinstance(v, int):
                        rt.update({k: rt.get(k) + v})
                else:
                    rt.update({k: v})
        return rt