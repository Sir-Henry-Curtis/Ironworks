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


class XbmcServer():

    def __init__(self):

        """Table for the XBMC server config"""
        # Check for ~/.ironworks
        if not os.path.isdir(configRootPath()):
            os.mkdir(configRootPath())

        self.configDb = ironworks.db.Db(os.path.join(configRootPath(), "config.db"))

        self.configDb.beginTransaction()

        self.configDb.checkTable("xbmc_servers", [
            {"name": "id", "type": "integer primary key autoincrement"},
            {"name": "label", "type": "text"},
            {"name": "position", "type": "integer"},
            {"name": "hostname", "type": "text"},
            {"name": "port", "type": "text"},
            {"name": "username", "type": "text"},
            {"name": "password", "type": "text"},
            {"name": "mac_address", "type": "text"}])

        self.configDb.commitTransaction()

        self.label = None
        self.position = None
        self.hostname = None
        self.port = None
        self.username = None
        self.password = None
        self.mac_address = None

    def __repr__(self):
        return '<XbmcServer %r>' % (self.label)

    def getNumXbmcServers(self):
        serverList = self.configDb.select("xbmc_servers")
        servers = serverList.fetchall()
        servers = len(servers)
        return servers

    def xbmcServer(self, label, position, hostname, port='8080', username=None, password=None, mac_address=None):
        self.label = label

        if position is None:
            self.position = highest_position(Disk)
        else:
            self.position = position

        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.mac_address = mac_address
