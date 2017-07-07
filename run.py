'''
    此处存放后台接口，由于目前接口较少
'''
import logging
from flask import render_template, jsonify
from initial import app
from test_method.caseOperator import apiFunc
from common.function import Operator
import os
from datetime import datetime
from flask import send_file
from common.time_handle import handle
from db_operator.mysql_db import MysqlDb
from flask import request
import re
from db_operator.user_db import UserDb
from flask import session
from flask import url_for
from flask import redirect
from datetime import timedelta
from db_operator.mongo_operator import MongoClient
from flask import make_response



'''
# 运行excel文件用例接口
@app.route('/run/<filename>', methods=['GET'])
def run_test(filename):
    rt, report = {}, None
    try:
        # 获取excel工作目录
        dir = app.config['WORKSPACE']
        obj = apiFunc()
        rt = obj.run_test(dir, [filename], app.config['THREAD_NUM'])
        report = obj.writeReport(rt)
    except Exception as err:
        logging.error("run_test error: {}".format(str(err)))
    return render_template('testResult.html',failNum=rt['failed_num'], ignored=rt['ignored'],
                           successNum=rt['success_num'], total=rt['total'], start=rt['start'],
                           end=rt['end'], cost="{:.2}秒".format(rt['cost']), fileName=report)
'''


@app.route('/', methods=['GET'])
def index():
    if session.get('user'):
        return render_template('index.html', user=session.get('user'))
    else:
        return redirect(url_for('for_login'))


@app.route('/case')
def case_view():
    if session.get('user'):
        db = MongoClient()
        caseList = db.get_case_list()
        del db
        return render_template('case_list.html', posts=caseList, user=session.get('user'))
    else:
        return redirect(url_for('for_login'))


# 运行excel文件用例接口
@app.route('/run', methods=['POST'])
def run_selected():
    excel_list = []
    start = handle.now_str()
    form_data = request.form.__str__()
    # 正则提取选中的excel
    if re.findall(r'\[(.+)\]', form_data):
        rv = re.findall(r'\[(.+)\]', form_data)[0]
        rv = re.findall(r'\((.+?)\)', rv)
        for item in rv:
            excel_list.append(item.split(',')[-1].replace("\'","").replace("\\\\", "\\").split()[0])
    rt, report = {}, None
    try:
        # 获取excel工作目录
        dir = app.config['WORKSPACE']
        obj = apiFunc()
        if excel_list:
            rt = obj.run_test(dir, excel_list, app.config['THREAD_NUM'])
            report = obj.writeReport(rt)
        else:
            return render_template("error.html", errorInfo="请选择至少一个xlsx文件! 页面会在3秒后跳转!")
    except Exception as err:
        logging.error("run_test error: {}".format(str(err)))
    return render_template('testResult.html',failNum=rt['failed_num'], ignored=rt['ignored'],
                           successNum=rt['success_num'], total=rt['total'], start=start,
                           end=handle.now_str(), cost="{:.2}秒".format(handle.delta(start, handle.now_str())),
                           fileName=report)


# 查看报告接口
@app.route('/report/<filename>')
def showHtml(filename):
    return send_file(os.path.join(app.config['REPORT'], filename))


# 查询验证码并返回
@app.route('/getVerifyCode')
def getVerify(mobile="18516600716"):
    rt = {'code': None}
    db = MysqlDb(app.config['DBNAME'])
    rt.update(dict(code=db.getVerifyCode(mobile)))
    return jsonify(rt)


@app.route('/delUser')
def delUser(mobile="18516600716"):
    rt = {'status': False}
    db = MysqlDb(app.config['DBNAME'])
    rt.update(dict(status=db.delete_user(mobile)))
    return jsonify(rt)


@app.route('/case/new', methods=['POST'])
def create_case():
    if session.get('user'):
        db = None
        rt = {'code': 500, 'error': '', 'status': 0}
        case_info = {}
        try:
            data = request.form
            if data:
                expect = data.get('expected')
                case_name = str(data.get('case_name'))
                params = data.get('params')
                method = data.get('method')
                _assert = data.get('assert')
                url = data.get('url')
                headers = data.get('headers')
                content = data.get('content', '')
                precondition = data.get("precondition")
                sql_prepare = data.get('sql_prepare')
                sql_verify = data.get('sql_verify')
                sql_clean = data.get('sql_clean')
                case_info.update(dict(
                    expected=expect, enable=True,
                    name=case_name, params=params,
                    _assert=_assert, url=url,
                    content=content, method=method,
                    headers=headers, sql_clean=sql_clean,
                    sql_verify=sql_verify, sql_prepare=sql_prepare,
                    pre=precondition
                ))
                case_info = Operator.transfer_str(**case_info)
                if expect and case_name and method and url and headers:
                    if method.lower() == 'post':
                        if not params:
                            raise Exception('Please provide params for post method.')
                    db = MongoClient()
                    result = db.add_case(**case_info)
                    if result:
                        rt.update(dict(code=200, status=1, msg='Add a case Successfully.'))
                else:
                    raise Exception('Please check your params for case_info.')
        except Exception as err:
            logging.error('create_case error: {}'.format(str(err)))
            rt.update(dict(error=str(err)))
        finally:
            if db:
                del db
        return jsonify(rt)
    else:
        return redirect(url_for('for_login'))


@app.route('/create_case', methods=['GET'])
def create_case_html():
    if session.get('user'):
        return render_template('create_case.html', user=session.get('user'))
    else:
        return url_for('login.html', info=None)


@app.route('/run_xlsx')
def run_xlsx():
    if session.get('user'):
        file_list = Operator.getFileList()
        return render_template('run_xlsx.html', fileList=file_list, user=session.get('user'))
    else:
        return redirect(url_for('for_login'))


@app.route('/login', methods=('POST', ))
def login():
    db = UserDb(app.config['LOCAL_DB'])
    form = request.form
    user = form.get('user')
    pwd = form.get('pwd')
    password = db.login(user)
    del db
    if pwd == password:
        # 添加登陆状态
        session.permanent = True
        # session保留时间
        app.permanent_session_lifetime = timedelta(minutes=30)
        session.update(dict(user=user))
        return render_template('index.html')
    elif password is None:
        return render_template('login.html', info="该用户不存在!")
    else:
        return render_template('login.html', info="密码不正确!")


@app.route('/for_login')
def for_login():
    if session.get('user'):
        return render_template('index.html', info=None, user=session.get('user'))
    else:
        return render_template('login.html')

@app.route('/for_register')
def for_register():
    return render_template('register.html', info=None)


@app.route('/register', methods=('POST', ))
def register():
    form = request.form
    user = form.get('user')
    pwd = form.get('passwd1')
    db = UserDb(app.config['LOCAL_DB'])
    rt = db.register(user, pwd)
    if rt:
        session.update(dict(user=user))
        return render_template('register_to_main.html')
    else:
        return render_template('register.html', info='用户已存在!')


@app.route('/delete_case', methods=('POST', ))
def delete_case():
    rt = {'status': False, 'msg': None}
    try:
        data = request.get_json()
        case_name = data.get('case_name')
        db = MongoClient()
        db.delete_case(case_name)
        del db
        rt.update(dict(status=True))
    except Exception as err:
        print("{} error: {}".format(Operator.get_current_func(), str(err)))
    return jsonify(rt)


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect(url_for("for_login"))


@app.route("/run_case", methods=('POST', ))
def run_selected_case():
    # return jsonify(dict(name='selenium'))

    data = request.get_json()
    start = handle.now_str()
    # 先找到mongo里的case信息
    db = MongoClient()
    case_list = db.get_case_by_name(data.get('case_name'))
    obj = apiFunc()
    rt = obj.run_tests(case_list, app.config['THREAD_NUM'])
    report = obj.writeReport(rt)
    html = render_template('testResult.html',failNum=rt['failed_num'], ignored=rt['ignored'],
                           successNum=rt['success_num'], total=rt['total'], start=start,
                           end=handle.now_str(), cost="{:.2}秒".format(handle.delta(start, handle.now_str())),
                           fileName=report)
    return jsonify(dict(html=html))


@app.route("/homework")
def get_homework():
    if session.get('user'):
        obj = MongoClient()
        db = obj.get_db()
        homework = list(db.homework.find())
        return render_template('homework.html', user=session.get('user'), homework=homework)
    else:
        return render_template('login.html')


@app.route("/homework/download/<filename>")
def download_homework(filename):
    return send_file(os.path.join(app.config['HOMEWORK'], filename))


@app.route("/edit_case/<case_name>")
def edit_page(case_name):
    db = MongoClient()
    case = db.get_case_info(case_name)
    case = Operator.transfer_case_info(case)
    return render_template('edit_case.html', case=case)


@app.route("/case/edit", methods=('POST', ))
def edit_case():
    if session.get('user'):
        db = None
        rt = {'code': 500, 'error': '', 'status': 0}
        case_info = {}
        try:
            data = request.form
            if data:
                _id = data.get('_id')
                expect = data.get('expected')
                case_name = str(data.get('case_name'))
                params = data.get('params')
                method = data.get('method')
                _assert = data.get('assert')
                url = data.get('url')
                headers = data.get('headers')
                content = data.get('content', '')
                precondition = data.get("precondition")
                sql_prepare = data.get('sql_prepare')
                sql_verify = data.get('sql_verify')
                sql_clean = data.get('sql_clean')
                case_info.update(dict(
                    expected=expect, enable=True,
                    name=case_name, params=params,
                    _assert=_assert, url=url,
                    content=content, method=method,
                    headers=headers, sql_clean=sql_clean,
                    sql_verify=sql_verify, sql_prepare=sql_prepare,
                    pre=precondition
                ))
                case_info = Operator.transfer_str(**case_info)
                if expect and case_name and method and url and headers:
                    if method.lower() == 'post':
                        if not params:
                            raise Exception('Please provide params for post method.')
                    db = MongoClient()
                    result = db.edit_case(_id, case_info)
                    if result.raw_result['ok']:
                        rt.update(dict(code=200, status=1, msg='Add a case Successfully.'))
                else:
                    raise Exception('Please check your params for case_info.')
        except Exception as err:
            logging.error('create_case error: {}'.format(str(err)))
            rt.update(dict(error=str(err)))
        finally:
            if db:
                del db
        return jsonify(rt)
    else:
        return redirect(url_for('for_login'))


@app.route('/people')
def photos():
    return render_template("people.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)

