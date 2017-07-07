__author__ = 'Woody'
'''
    初始化app, 防止产生嵌套引用的问题
'''
from flask import Flask
from config import conf
import os
import logging
import requests
import json
from flask_sqlalchemy import SQLAlchemy


def getToken():
    data = {
        "actionTime": "2017-06-12 15:00:00",
        "appId": 1009,
        "requestData": {
            "areaCode": 86,
            "mobile": "18516600716",
            "password": "wuranxu"
        }
    }
    headers = {"Content-Type": "application/json"}
    p = requests.post("http://devapi2017.yitu8.cn/client/user/userLogin", json=data, headers=headers)
    data = json.loads(p.text)
    return data.get('responseData').get('token')


app = Flask(__name__)
# 从config.py获取配置
config_obj = conf()
app.config.from_object(config_obj)
# app.config['TOKEN'] = getToken()
db = SQLAlchemy(app)

# 配置日志文件
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=os.path.join(app.config['LOG_PATH'], app.config['LOG_NAME']),
                filemode='a+')

