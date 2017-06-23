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

    # 时间格式
    TIMEFORMAT = "%Y-%m-%d %H:%M:%S"

    # 报告目录
    REPORT = os.path.join(ROOT, 'report')

    # 线程个数
    THREAD_NUM = 10
