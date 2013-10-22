# -*- coding: utf-8 -*-
from flask import render_template, session
from Ironworks import app
from ironworks.noneditable import *
from modules.bleextop import settingsLogin
from ironworks.models import xbmcServer, setting
from ironworks import logger, tools, preferences
from modules import *


@app.route('/currentHouse')
def currentHouse():
    if 'username' in session:
        houses = []
        return render_template('currentHouse.html',
            houses=houses)
    return render_template('index.html')