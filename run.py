'''
    此处存放后台接口，由于目前接口较少
'''
import logging
from flask import render_template, jsonify
from initial import app
from test_method.caseOperator import apiFunc
import os
from datetime import datetime
from flask import send_file
from common.time_handle import handle

@app.route('/')
def hello_world():
    return '正在运行!'


# 运行excel文件用例接口
@app.route('/run/<filename>', methods=['GET'])
def run_test(filename):
    rt, report = {}, None
    try:
        # 获取excel工作目录
        dir = app.config['WORKSPACE']
        obj = apiFunc()
        rt = obj.run_test(dir, filename, app.config['THREAD_NUM'])
        report = obj.writeReport(rt)
    except Exception as err:
        logging.error("run_test error: {}".format(str(err)))
    return render_template('testResult.html',failNum=rt['failed_num'], ignored=rt['ignored'],
                           successNum=rt['success_num'], total=rt['total'], start=rt['start'],
                           end=rt['end'], cost="{:.2}秒".format(rt['cost']), fileName=report)


# 查看报告接口
@app.route('/report/<filename>')
def showHtml(filename):
    return send_file(os.path.join(app.config['REPORT'], filename))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
