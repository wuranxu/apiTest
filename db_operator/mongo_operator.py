__author__ = 'Woody'
import pymongo
from initial import app
import logging
from bson import ObjectId


class MongoClient(object):
    HOST = app.config['MONGO_HOST']
    PORT = app.config['MONGO_PORT']
    user = app.config['MONGO_USER']
    pwd = app.config['MONGO_PWD']

    def __init__(self):
        try:
            self.Client = pymongo.MongoClient(host=self.HOST, port=self.PORT)
            self.db = self.Client.yitu8
            assert self.db.authenticate(self.user, self.pwd), "mongo服务器连接失败!"
        except Exception as err:
            logging.error("mongo connect error: {}".format(str(err)))

    def __del__(self):
        self.Client.close()

    def add_case(self, **kwargs):
        return self.db.test_case.insert_one(kwargs)

    def edit_case(self, _id, case_info):
        return self.db.test_case.update_one({"_id": ObjectId(_id)}, {"$set": case_info})

    def delete_case(self, name):
        self.db.test_case.delete_many({"name": {"$in": name}})

    def get_case_list(self):
        case_list = self.db.test_case.find()
        return list(case_list)

    def get_case_by_name(self, name_list):
        case_list = self.db.test_case.find({"name": {"$in": name_list}})
        return list(case_list)

    def get_db(self):
        return self.db

    def get_case_info(self, case_name):
        return self.db.test_case.find_one({"name": case_name})
