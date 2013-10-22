# -*- coding: utf-8 -*-
from flask import g
from ironworks import tools


class UserDAO:

    def __init__(self):
        tools.setDb
        self.db = g.get('db')

    def validate(self, data):
        result = self.db.select("users", where=data)
        return result

    def getUser(self, data):
        result = self.db.select("users", where=data)
        user = result[0]
        userDict = {}
        userDict["user_k"] = str(user[0])
        userDict["username"] = user[1]
        userDict["email"] = user[3]
        userDict["name"] = user[4]
        userDict["lastname"] = user[5]
        userDict["avatar"] = user[6]
        userDict["active"] = user[7]
        return userDict

    def getAllUsers(self, limit=(0, 25)):
        result = self.db.query("select U.*,(select count(*) from users) as total from users U limit ?,?", tuple=limit)
        return result