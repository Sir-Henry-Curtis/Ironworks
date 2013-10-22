# -*- coding: utf-8 -*-
import sys
import os
import shutil
import datetime

from flask import g
from ironworks import preferences, tools
from bleextop.libraries import applicationbi


class Bleex:

    def __init__(self):
        tools.setDb()
        self.db = g.get('db')
        self.app = applicationbi.ApplicationBI
        self.prefs = preferences.Prefs()

        self.db.beginTransaction()

        self.db.checkTable("applications", [
            {"name": "application_k", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
            {"name": "application_parent_k", "type": "int"},
            {"name": "name", "type": "varchar(200)"},
            {"name": "description", "type": "text"},
            {"name": "klass", "type": "varchar(255)"},
            {"name": "configurations", "type": "text"},
            {"name": "date_created", "type": "datetime"},
            {"name": "date_updated", "type": "datetime"},
            {"name": "active", "type": "tinyint(1)"}])

        self.db.checkTable("permissions", [
            {"name": "permission_k", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
            {"name": "application_k", "type": "int"},
            {"name": "action", "type": "varchar(50)"},
            {"name": "name", "type": "varchar(100)"},
            {"name": "description", "type": "text"}], [
            "application_k"])

        self.db.checkTable("role_permissions", [
            {"name": "role_permission_k", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
            {"name": "role_k", "type": "int"},
            {"name": "permission_k", "type": "int"},
            {"name": "value", "type": "tinyint(1)"},
            {"name": "date_created", "type": "datetime"}], [
            "role_k",
            "permission_k"])

        self.db.checkTable("roles", [
            {"name": "role_k", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
            {"name": "name", "type": "varchar(50)"},
            {"name": "description", "type": "text"}])

        self.db.checkTable("user_permissions", [
            {"name": "user_permission_k", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
            {"name": "user_k", "type": "int"},
            {"name": "permission_k", "type": "int"},
            {"name": "value", "type": "int"},
            {"name": "date_created", "type": "datetime"}], [
            "user_k",
            "permission_k"])

        self.db.checkTable("user_roles", [
            {"name": "user_k", "type": "int"},
            {"name": "role_k", "type": "int"},
            {"name": "date_created", "type": "datetime"}], [
            "user_k",
            "role_k"])

        self.db.checkTable("users", [
            {"name": "user_k", "type": "INT PRIMARY KEY AUTO_INCREMENT"},
            {"name": "username", "type": "varchar(20)"},
            {"name": "password", "type": "varchar(32)"},
            {"name": "email", "type": "varchar(100)"},
            {"name": "name", "type": "varchar(50)"},
            {"name": "lastname", "type": "varchar(50)"},
            {"name": "avatar", "type": "varchar(255)"},
            {"name": "active", "type": "tinyint(1)"}], [
            "username"])

        # Check basic defaults
        #Applications
        self.checkDesktopDefaults("applications", data={
                                                        "name": "Administration",
                                                        "description": "Administration Folder",
                                                        "configurations": '{"iconCls":"","width":800,"height":480,"shorcutIconCls":""}',
                                                        "date_created": "2011-08-09 11:03:53",
                                                        "date_updated": "2011-08-09 11:03:53",
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_parent_k": '1',
                                                        "name": 'Applications',
                                                        "description": 'Applications Catalog',
                                                        "klass": 'Bleext.modules.catalogs.applications.controller.Application',
                                                        "configurations": '{"iconCls":"applications-icon"}',
                                                        "date_created": '2011-08-09 11:03:53',
                                                        "date_updated": '2011-08-09 11:03:53',
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_parent_k": '1',
                                                        "name": 'Roles',
                                                        "description": 'Roles Catalog',
                                                        "klass": 'Bleext.modules.catalogs.roles.controller.Roles',
                                                        "configurations": '{"iconCls":"roles-icon","width":800,"height":480,"shorcutIconCls":""}',
                                                        "date_created": '2011-08-09 11:03:53',
                                                        "date_updated": '2011-08-09 11:16:10',
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_parent_k": '1',
                                                        "name": 'Users',
                                                        "description": 'Users Module',
                                                        "klass": 'Bleext.modules.catalogs.users.controller.Users',
                                                        "configurations": '{"iconCls":"users-icon","shorcutIconCls":"roles-app-shorcut-icon","width":800,"height":480}',
                                                        "date_created": '2011-08-09 11:03:53',
                                                        "date_updated": '2011-08-09 10:57:29',
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_parent_k": '1',
                                                        "name": 'Privileges',
                                                        "description": 'This module allow you to set the privileges to the roles and applications',
                                                        "klass": 'Bleext.modules.security.permissions.controller.Permission',
                                                        "configurations": '{"iconCls":"permissions-icon-16","width":800,"height":480,"shorcutIconCls":""}',
                                                        "date_created": '2011-08-09 11:03:53',
                                                        "date_updated": '2011-10-26 07:50:40',
                                                        "active": "1"})
        self.checkDesktopDefaults("applications", data={
                                                        "application_parent_k": '1',
                                                        "name": 'Groups',
                                                        "description": 'Groups Module',
                                                        "klass": 'Bleext.modules.security.groups.controller.Groups',
                                                        "configurations": '{"iconCls":"groups-icon-16","width":800,"height":480,"shorcutIconCls":""}',
                                                        "date_created": '2011-10-26 08:03:28',
                                                        "date_updated": '2011-10-26 08:04:11',
                                                        "active": "1"})

        #Permissions
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '13',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'Permission Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '14',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'Permission to read all the applications'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '14',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '14',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '14',
                                                        "action": 'update',
                                                        "name": 'Update',
                                                        "description": 'Update Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '14',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '14',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '14',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '14',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '15',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'To Access the module'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '15',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '15',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '15',
                                                        "action": 'update',
                                                        "name": 'Update',
                                                        "description": 'Update Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '15',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '15',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '15',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '15',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '16',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'To appear in the menu'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '16',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '16',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '16',
                                                        "action": 'update',
                                                        "name": 'Update',
                                                        "description": 'Update Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '16',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '16',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '16',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '16',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '17',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'Allow users to access the permissions module, this module should be visible only for administrators'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '17',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '17',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '17',
                                                        "action": 'update',
                                                        "name": 'Update',
                                                        "description": 'Update Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '17',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '17',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '17',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '17',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '18',
                                                        "action": 'access',
                                                        "name": 'Access',
                                                        "description": 'Groups Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '18',
                                                        "action": 'edit',
                                                        "name": 'Edit',
                                                        "description": 'Edit Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '18',
                                                        "action": 'create',
                                                        "name": 'Create',
                                                        "description": 'Create'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '18',
                                                        "action": 'list',
                                                        "name": 'List',
                                                        "description": 'List'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '18',
                                                        "action": 'delete',
                                                        "name": 'Delete',
                                                        "description": 'Delete Access'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '18',
                                                        "action": 'print',
                                                        "name": 'Print',
                                                        "description": 'Print'})
        self.checkDesktopDefaults("permissions", data={
                                                        "application_k": '18',
                                                        "action": 'export',
                                                        "name": 'Export',
                                                        "description": 'Export Access'})
        #Role Permissions
        #Administrator
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '81',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '82',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '83',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '84',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '85',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '86',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '87',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '88',
                                                        "value": '5',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '89',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '90',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '91',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '92',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '93',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '94',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '95',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '96',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '97',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '98',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '99',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '100',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '101',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '102',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '103',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '104',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '105',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '106',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '107',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '108',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '109',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '110',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '111',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '112',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '113',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '114',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '115',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '116',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '117',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '118',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '119',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '5',
                                                        "permission_k": '120',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        #User
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '84',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '85',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '86',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '87',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '88',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '89',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '90',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '98',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '113',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '114',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '115',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '116',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '117',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '118',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '119',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '6',
                                                        "permission_k": '120',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        #Visitor
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '84',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '85',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '86',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '87',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '88',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '89',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '90',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '98',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '113',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '114',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '115',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '116',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '117',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '118',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '119',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("role_permissions", data={
                                                        "role_k": '7',
                                                        "permission_k": '120',
                                                        "value": '0',
                                                        "date_created": '2011-08-05 17:35:39'})
        #Roles
        self.checkDesktopDefaults("roles", data={
                                                        "name": 'Administrator',
                                                        "description": 'The Super User'})
        self.checkDesktopDefaults("roles", data={
                                                        "name": 'Users',
                                                        "description": 'The Users Role'})
        self.checkDesktopDefaults("roles", data={
                                                        "name": 'Visitors',
                                                        "description": 'Visitors'})
        #User Permissions
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '81',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '82',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '83',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '84',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '85',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '86',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '87',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '88',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '89',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '90',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '91',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '92',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '93',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '94',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '95',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '96',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '97',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '98',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '99',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '100',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '101',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '102',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '103',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '104',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '105',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '106',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '107',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '108',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '109',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '110',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '111',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '112',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '113',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '114',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '115',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '116',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '117',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '118',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '119',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        self.checkDesktopDefaults("user_permissions", data={
                                                        "user_k": '1',
                                                        "permission_k": '120',
                                                        "value": '1',
                                                        "date_created": '2011-08-05 17:35:39'})
        #User Roles
        self.checkDesktopDefaults("user_roles", data={
                                                        "user_k": '1',
                                                        "role_k": '5',
                                                        "date_created": '2011-08-05 17:35:39'})
        #Users
        self.checkDesktopDefaults("users", data={
                                                        "username": 'admin',
                                                        "password": 'password',
                                                        "email": 'jlbrian7@gmail.com',
                                                        "name": "Admin",
                                                        "lastname": "Super",
                                                        "avatar": "default.png",
                                                        "active": "1"})

        self.db.commitTransaction()

    def checkDesktopDefaults(self, table, data):
        cursor = self.db.select(table, where=data)
        if not cursor:
            self.db.beginTransaction()
            self.db.insert(table, data)
            self.db.commitTransaction()
