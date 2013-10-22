# -*- coding: utf-8 -*-
import os
import sys

import ironworks.db


def configRootPath():
    if sys.platform == "darwin":
            return os.path.expanduser("~/Library/Application Support/ironworks")
    elif sys.platform.startswith("win"):
            return os.path.join(os.environ['APPDATA'], "ironworks")
    else:
            return os.path.expanduser("~/.ironworks")


def highest_position(model):
    highest_position = 0

    items = model.query.all()

    for item in items:
        if item.position > highest_position:
            highest_position = item.position

    return highest_position + 1


class Application():

    def __init__(self, name, url, description=None, image=None, position=None):

        """Table for one application in the applications module"""
        # Check for ~/.ironworks
        if not os.path.isdir(configRootPath()):
                os.mkdir(configRootPath())

        configDb = ironworks.db.Db(os.path.join(configRootPath(), "config.db"))

        configDb.beginTransaction()

        configDb.checkTable("applications", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "name", "type": "text"},
            {"name": "url", "type": "text"},
            {"name": "description", "type": "text"},
            {"name": "image", "type": "text"},
            {"name": "position", "type": "integer"}])

        configDb.commitTransaction()

        self.name = name
        self.url = url
        self.description = description
        self.image = image

        if position is None:
            self.position = highest_position(Application)
        else:
            self.position = position

    def __repr__(self):
        return '<Application %r>' % (self.name)