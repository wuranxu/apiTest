__author__ = 'Woody'
'''建立orm
'''

from run import db


class user(db.Model):
    userId = db.Column(db.INT, primary_key=True)
    phone = db.Column(db.String(255), unique=False)

    def __init__(self, userId, phone):
        self.userId = userId
        self.phone = phone

    def __repr__(self):
        return '<User %r>' % self.userId


class Orm(object):
    '''
    用法：
    obj = Orm()
    # 查询单条数据
    rt = obj.query_one(user, userId=1)

    # 查询多条数据
    users = obj.query(user, userId=1)

    # 更新数据
    obj.update(user, ('phone', '18516600716'), userId=1)

    # 添加数据
    new_user = user(2, '15021135862')
    obj.insert(new_user)

    # 删除数据
    obj.delete(obj.query_one(user, userId=2))

    '''

    def __init__(self):
        self.db = db

    def query_one(self, table, **filter):
        return self.db.session.query(table).filter_by(**filter).first()

    def query(self, table, **filter):
        return self.db.session.query(table).filter_by(**filter).all()

    def insert(self, obj):
        self.db.session.add(obj)
        self.db.session.commit()

    def update(self, table, *name, **filter):
        rv = self.db.session.query(table).filter_by(**filter).all()
        for item in rv:
            for key, value in name:
                setattr(item, key, value)
        self.db.session.commit()

    def delete(self, obj):
        self.db.session.delete(obj)
        self.db.session.commit()

