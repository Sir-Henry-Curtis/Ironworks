from flask import render_template
from ironworks import app, LOG_FILE
from ironworks.noneditable import *
from ironworks import logger
from pastebin.pastebin import PastebinAPI
from ironworks.tools import requires_auth
import ironworks

@app.route('/xhr/log')
@requires_auth
def xhr_log():
    return render_template('dialogs/log_dialog.html',
        log=ironworks.LOG_LIST,
    )


@app.route('/xhr/log/pastebin')
@requires_auth
def xhr_log_pastebin():
    file = open(LOG_FILE)
    log = []
    log_str = ''

    for line in reversed(file.readlines()):
        log.append(line.rstrip())
        log_str += line.rstrip()
        log_str += '\n'

    file.close()
    x = PastebinAPI()
    try:
        url = x.paste('feed610f82c2c948f430b43cc0048258', log_str)
        logger.log('LOG :: Log successfully uploaded to %s' % url, 'INFO')
    except Exception as e:
        logger.log('LOG :: Log failed to upload - %s' % e, 'INFO')

    return render_template('dialogs/log_dialog.html',
        log=log,
        url=url,
    )
