#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the main executable of Ironworks. It parses the command line arguments, does init and calls the start function of Ironworks."""

import sys
import os
import keyring
from flask import Flask


# Check if frozen by py2exe
def check_frozen():
    return hasattr(sys, 'frozen')


def get_rundir():
    if check_frozen():
        return os.path.abspath(unicode(sys.executable, sys.getfilesystemencoding()))

    return os.path.abspath(__file__)[:-13]


def ironworksRootPath():
    if sys.platform == "darwin":
            return os.path.expanduser("~/Library/Application Support/ironworks")
    elif sys.platform.startswith("win"):
            return os.path.join(os.environ['APPDATA'], "ironworks")
    else:
            return os.path.expanduser("~/.ironworks")


def checkDbKey():
    userName = 'sec_user'
    try:
        dbPassword = keyring.get_password("Ironworks-MySQL-" + userName, userName)
        if dbPassword is None:
            password = ''
            keyring.set_password("Ironworks-MySQL-" + userName, userName, password)
            app.logger.debug('entry added to keyring')
        elif dbPassword == '':
            app.logger.debug('password saved')
        else:
            app.logger.debug('unknown password')

    except:
        print 'error: either could not access keyring or an entry could not be made'


# Set the rundir
dataDir = ironworksRootPath()
if not os.path.isdir(ironworksRootPath()):
                os.mkdir(ironworksRootPath())
rundir = get_rundir()

# Include paths
sys.path.insert(0, rundir)
sys.path.insert(0, os.path.join(rundir, 'lib'))

# Create Flask instance
app = Flask(__name__)
app.secret_key = 'your secret key goes here'

# If frozen, we need define static and template paths
if check_frozen():
    app.root_path = rundir
    app.static_path = '/static'
    app.add_url_rule(
        app.static_path + '/<path:filename>',
        endpoint='static',
        view_func=app.send_static_file
    )

    from jinja2 import FileSystemLoader
    app.jinja_loader = FileSystemLoader(os.path.join(rundir, 'templates'))


def import_modules():
    """All modules that are available in Ironworks are at this point imported."""
    from modules.home import controls
    from modules.home import currently_playing
    import modules.index
    import modules.log
    from modules.home import remote
    import modules.search
    #import modules.updater
    import modules.xbmc_notify


@app.teardown_request
def shutdown_session(exception=None):
    """This function is called as soon as a session is shutdown and makes sure, that the db session is also removed."""
    from ironworks.database import db_session
    db_session.remove()

import ironworks
import ironworks.preferences


class ironworksMain():
    def __init__(self):
        """Main function that is called at the startup of Ironworks."""
        self.started = False
        self.prefs = ironworks.preferences.Prefs()

        from optparse import OptionParser

        p = OptionParser()

        # define command line options
        p.add_option('-p', '--port',
                     dest='port',
                     default=None,
                     help="Force webinterface to listen on this port")
        p.add_option('-d', '--daemon',
                     dest='daemon',
                     action='store_true',
                     help='Run as a daemon')
        p.add_option('--pidfile',
                     dest='pidfile',
                     help='Create a pid file (only relevant when running as a daemon)')
        p.add_option('--log',
                     dest='log',
                     help='Create a log file at a desired location')
        p.add_option('-v', '--verbose',
                     dest='verbose',
                     action='store_true',
                     help='Silence the logger')
        p.add_option('--develop',
                     action="store_true",
                     dest='develop',
                     help="Start instance of development server")
        p.add_option('--database',
                     dest='database',
                     help='Custom database file location')
        p.add_option('--webroot',
                     dest='webroot',
                     help='Web root for Ironworks')
        p.add_option('--host',
                     dest='host',
                     help='Web host for Ironworks')
        p.add_option('--kiosk',
                     dest='kiosk',
                     action='store_true',
                     help='Disable settings in the UI')
        p.add_option('--datadir',
                     dest='datadir',
                     help='Write program data to custom location')
        p.add_option('--noupdate',
                     action="store_true",
                     dest='noupdate',
                     help='Disable the internal updater')

        # parse command line for defined options
        options, args = p.parse_args()

        if options.datadir:
            data_dir = options.datadir
        else:
            data_dir = dataDir

        if options.daemon:
            ironworks.DAEMON = True
            ironworks.VERBOSE = False
        else:
            val = self.prefs.getDaemon()
            if val == "True":
                ironworks.DAEMON = True
                ironworks.VERBOSE = False

        if options.pidfile:
            ironworks.PIDFILE = options.pidfile
            ironworks.VERBOSE = False
        else:
            val = self.prefs.getPidFile()
            if val == "True":
                ironworks.PIDFILE = self.prefs.getPidFilName()
                ironworks.VERBOSE = False

        if options.port:
            PORT = int(options.port)
        else:
            PORT = self.prefs.getPort()  # 7000

        if options.log:
            ironworks.LOG_FILE = options.log

        if options.verbose:
            ironworks.VERBOSE = True
        else:
            val = self.prefs.getVerbose()
            if val == "True":
                ironworks.VERBOSE = True

        if options.develop:
            ironworks.DEVELOPMENT = True
        else:
            val = self.prefs.getDevelopment()
            if val == "True":
                ironworks.DEVELOPMENT = True

        if options.database:
            DATABASE = options.database
        else:
            DATABASE = os.path.join(dataDir, 'ironworks.db')

        if options.webroot:
            ironworks.WEBROOT = options.webroot

        if options.host:
            ironworks.HOST = options.host

        if options.kiosk:
            ironworks.KIOSK = True
        else:
            val = self.prefs.getKiosk()
            if val == "True":
                ironworks.KIOSK = True

        if options.noupdate:
            ironworks.UPDATER = False
        else:
            val = self.prefs.getNoUpdate()
            if val == "True":
                ironworks.UPDATER = False

        ironworks.RUNDIR = rundir
        ironworks.DATA_DIR = data_dir
        ironworks.FULL_PATH = os.path.join(rundir, 'ironworks.py')
        ironworks.ARGS = sys.argv[1:]
        ironworks.PORT = PORT
        ironworks.DATABASE = DATABASE

        checkDbKey()

        ironworks.initialize()

        if ironworks.PIDFILE or ironworks.DAEMON:
            ironworks.daemonize()

        import_modules()
        ironworks.init_updater()

        ironworks.start()


if __name__ == '__main__':
    ironworksApp = ironworksMain()
