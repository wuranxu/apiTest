__author__ = 'woody'
'''配置类
'''
import os


class conf(dict):
    # 系统根目录
    ROOT = r'E:\ApiTest'

    # 存放excel文件的目录
    WORKSPACE = os.path.join(ROOT, 'excel_data')

    # 存放日志的目录
    LOG_PATH = os.path.join(ROOT, 'log')

    # 日志名
    LOG_NAME = 'ApiTest.log'

    # 日志配置文件
    LOG_CONFIG = os.path.join(WORKSPACE, 'api_config.xlsx')

    # 用例超时时间
    TIMEOUT = 10

    # SQLALCHEMY关联数据库地址
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:wuranxu@localhost:3306/test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 时间格式
    TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

    # 报告目录
    REPORT = os.path.join(ROOT, 'report')

    # 线程个数
    THREAD_NUM = 1

    # excel配置文件
    CONFIG_XLSX = 'api_config.xlsx'

    # mysql地址
    HOST = "devapi2017.yitu8.cn"

    # mysql端口
    PORT = 3306

    # mysql用户名
    MYSQL_USER = 'yitu8v3'

    # mysql密码
    MYSQL_PWD = 'Yitu8@v3'

    # mysql 验证码表
    MESSAGE_TABLE = 'yt8_sms_log'

    # USER表
    USER_TABLE = 'yt8_user'

    # 数据库名
    DBNAME = 'yitu8v3'

    # tester账户
    TESTER = '18516600716'

    LOCAL_HOST = 'localhost'
    LOCAL_PORT = '3306'
    LOCAL_USER = 'root'
    LOCAL_PWD = 'wuranxu'
    LOCAL_DB = 'test'
    CASE_TABLE = 'api'
    LOCAL_USER_TABLE = 'user'
    SECRET_KEY = 'xxx'

    # mongo config
    MONGO_HOST = '127.0.0.1'
    MONGO_PORT = 27017
    MONGO_USER = 'yitu8'
    MONGO_PWD = 'yitu8'

    HOMEWORK = os.path.join(ROOT, 'homework')