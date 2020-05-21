import os
import sys
from orator import DatabaseManager

path = os.path.join(sys.path[0], "data", "database")

config = {
    'sqlite': {
        'driver': 'sqlite',
        'database': path,
        'foreign_keys': False
    }
}

db = DatabaseManager(config)


class Db(object):
    def __init__(self):
        super(Db, self).__init__()

    @staticmethod
    def check_user(user_id):
        return db.table("users").where("user_id", "=", user_id).count()

    @staticmethod
    def user_info(user_id):
        return db.table("users").where("user_id", "=", user_id).first()

    @staticmethod
    def insertUser(user_info):
        if not Db.check_user(user_info['user_id']):
            return db.table("users").insert(user_info)
        else:
            return

    @staticmethod
    def usersCount():
        return db.table("users").count()

    @staticmethod
    def addNewAdmin(user_info):
        return db.table('user_role').inser(user_info)

    @staticmethod
    def updateRole(user_id, role):
        return db.table('user_role').where("user_id", "=", user_id).update(role=role)

    @staticmethod
    def insertOrder(order_info):
        db.table('orders').insert(order_info)
        return db.table('orders').select('id').order_by('id', 'desc').first()

    @staticmethod
    def blockUser(user_id):
        return db.table('users').where("user_id", "=", user_id).update(block=1)

    @staticmethod
    def unblockUser(user_id):
        return db.table('users').where("user_id", "=", user_id).update(block=0)
