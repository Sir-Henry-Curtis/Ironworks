# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request, session
import hashlib, random, urllib
from ironworks.noneditable import *
from ironworks.modules import *
from ironworks.tools import requires_auth, get_setting_value
import ironworks
from ironworks import logger, preferences
import ironworks.db
from ironworks.models import XbmcServer
import sys
import os


@app.route('/feeds')
def feeds():
    if 'username' in session:
        return render_template('feeds.html')
    return 'You are not logged in'