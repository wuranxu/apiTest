__author__ = 'Woody'
import mysql.connector as mysql
from initial import app
import logging
import re
from db_operator.mysql_db import MysqlDb


class UserDb(MysqlDb):
    host = app.config['LOCAL_HOST']
    port = app.config['LOCAL_PORT']
    username = app.config['LOCAL_USER']
    pwd = app.config['LOCAL_PWD']
    # dbname = app.config['LOCAL_DB']
    user_table = app.config['LOCAL_USER_TABLE']

    def login(self, user):
        sql = "select password from {} where username='{}'".format(self.user_table, user)
        rv = self.query(sql)
        if rv:
            return rv[0][0]
        else:
            return None

    def register(self, user, pwd):
        sql = 'INSERT INTO {} (username, password) VALUES ("{}", "{}")'.format(self.user_table, user, pwd)
        return self.operator(sql)
