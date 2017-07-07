__author__ = 'Woody'
import mysql.connector as mysql
from initial import app
import logging
import re


class MysqlDb(object):
    host = app.config['HOST']
    port = app.config['PORT']
    username = app.config['MYSQL_USER']
    pwd = app.config['MYSQL_PWD']
    sms_table = app.config['MESSAGE_TABLE']
    user_table = app.config['USER_TABLE']

    def __init__(self, dbname):
        self.connection = mysql.connect(
                host=self.host, port=self.port, user=self.username,
                password=self.pwd, db=dbname
            )

    def query(self, sql, params=()):
        rv = None
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            rv = cursor.fetchall()
        except Exception as err:
            logging.error('query error: {}'.format(str(err)))
            print(str(err))
        finally:
            if cursor:
                cursor.close()
        return rv

    def operator(self, sql, params=()):
        rv = False
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, params)
            self.connection.commit()
            rv = True
        except Exception as err:
            logging.error('query error: {}'.format(str(err)))
            print(str(err))
        finally:
            if cursor:
                cursor.close()
        return rv


    def getVerifyMsg(self, mobile):
        return

    def getVerifyCode(self, mobile=app.config['TESTER']):
        sql = 'select smsBody from {} where mobile=%s order by smsLogId desc limit 1'.format(self.sms_table)
        rv = self.query(sql, params=(mobile, ))
        msg = rv[0][0] if rv else None
        if msg:
            rt = re.findall(r'[\d]+', msg)
            if rt:
                return rt[0]
            else:
                return None

    def delete_user(self, mobile=app.config['TESTER']):
        sql = "delete from {} where phone={}".format(self.user_table, mobile)
        rt = self.operator(sql)
        return rt

    def verify_user(self, mobile=app.config['TESTER']):
        sql = "select * from {} where phone={}".format(self.user_table, mobile)
        rt = self.query(sql)
        if rt:
            if rt[0] is not None:
                return True
        return False

    def __del__(self):
        self.connection.close()