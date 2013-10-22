
from flask import jsonify, render_template, request, session, g
from ironworks.noneditable import *
from ironworks.modules import *
from ironworks import bleex, tools
from modules import settings
import sys
import os


def configRootPath():
    if sys.platform == "darwin":
        return os.path.expanduser("~/Library/Application Support/ironworks")
    elif sys.platform.startswith("win"):
        return os.path.join(os.environ['APPDATA'], "ironworks")
    else:
        return os.path.expanduser("~/.ironworks")


def validate(db, user, password):
    success = False
    isValid = db.select("users", where={"username": user, "password": password})
    if isValid:
        success = True
        tools.setUser(user)
    return success


def createLogin(db, user, password):
    success = False
    db.insertOrUpdate("users", {"username": user, "password": password})
    isValid = db.select("users", where={"username": user})
    if isValid:
        success = True
    return success


@app.route('/settingsLogin')
def settingsLogin():
    if 'username' in session:
        bleex.Bleex()
        return render_template('settingsLogin.html')
    return render_template('index.html')


@app.route('/settings_login', methods=['GET', 'POST'])
def settings_login():
    tools.setDb()
    db = g.get('db')
    success = False

    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']

        success = validate(db, user, password)

    if success:
        return jsonify(success=success)
    return render_template('settingsLogin.html')


@app.route('/settings_create_login', methods=['GET', 'POST'])
def settings_create_login():
    db = g.get('db')
    success = False

    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']

        success = createLogin(db, user, password)

    if success:
        return jsonify(success=success)
    return render_template('settingsLogin.html')