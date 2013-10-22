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


class Module():

    def __init__(self, name, column, position=None, poll=None, delay=None):
        """Table for one Ironworks module"""
        # Check for ~/.ironworks
        if not os.path.isdir(configRootPath()):
                os.mkdir(configRootPath())

        configDb = ironworks.db.Db(os.path.join(configRootPath(), "config.db"))

        configDb.beginTransaction()

        configDb.checkTable("modules", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "name", "type": "text"},
            {"name": "column", "type": "integer"},
            {"name": "position", "type": "integer"},
            {"name": "poll", "type": "integer"},
            {"name": "delay", "type": "integer"}])

        configDb.commitTransaction()

        self.name = name
        self.column = column
        self.position = position
        self.poll = poll
        self.delay = delay

    def __repr__(self):
        return '<Module %r>' % (self.name)
