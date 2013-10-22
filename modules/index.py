from flask import render_template, request, session, redirect, url_for

import hashlib
import keyring
import MySQLdb
import time

from Ironworks import app
from ironworks.noneditable import *
from modules.home import latestNews
import ironworks
import ironworks.db


def login(email, password, dbConn):
    # Using prepared Statements means that SQL injection is not possible.
    c = dbConn.cursor()
    if c.execute("""SELECT id, username, password, salt FROM members WHERE email = %s LIMIT 1""", (email, )) is not None:
        # (id, username, email, password, salt)
        result = c.fetchone()
        user_id = result[0]
        username = result[1]
        db_password = result[2]
        salt = result[3]
        #print result, user_id, username, db_password, salt
        password = hashlib.sha512(password + salt).hexdigest()  # hash the password with the unique salt.
        # print password
        if checkbrute(user_id, dbConn) is True:
            # Account is locked
            # Send an email to user saying their account is locked
            return False
        elif db_password == password:  # Check if the password in the database matches the password the user submitted.
            # Password is correct!
            session['username'] = username
            #print 'Login successful.'
            return True
        else:
            # Password is not correct
            # We record this attempt in the database
            #print 'fail'
            now = int(time.time())
            c.execute("INSERT INTO login_attempts (user_id, time) VALUES (%s, %s)", (user_id, now))
            return False
    else:
        # No user exists.
        return False


def checkbrute(user_id, dbConn):
    c = dbConn.cursor()
    # Get timestamp of current time
    now = int(time.time())
    delta = 7200
    # All login attempts are counted from the past 2 hours.
    valid_attempts = now - delta
    # print valid_attempts
    if c.execute("SELECT time FROM login_attempts WHERE user_id = %s AND time > '%s'", (user_id, valid_attempts)) is not None:
        # Execute the prepared query.
        attempts = c.fetchall()
        # If there has been more than 5 failed logins
        if len(attempts) > 5:
            return True
        else:
            return False

'''def login_check(dbConn):
    # Check if all session variables are set
   if(isset($_SESSION['user_id'], $_SESSION['username'], $_SESSION['login_string'])) {
     $user_id = $_SESSION['user_id'];
     $login_string = $_SESSION['login_string'];
     $username = $_SESSION['username'];

     $user_browser = $_SERVER['HTTP_USER_AGENT']; // Get the user-agent string of the user.

     if ($stmt = $mysqli->prepare("SELECT password FROM members WHERE id = ? LIMIT 1")) {
        $stmt->bind_param('i', $user_id); // Bind "$user_id" to parameter.
        $stmt->execute(); // Execute the prepared query.
        $stmt->store_result();

        if($stmt->num_rows == 1) { // If the user exists
           $stmt->bind_result($password); // get variables from result.
           $stmt->fetch();
           $login_check = hash('sha512', $password.$user_browser);
           if($login_check == $login_string) {
              // Logged In!!!!
              return true;
           } else {
              // Not logged in
              return false;
           }
        } else {
            // Not logged in
            return false;
        }
     } else {
        // Not logged in
        return false;
     }
   } else {
     // Not logged in
     return false;
   }'''


@app.route('/')
def index():
    return render_template('index.html',
        webroot=ironworks.WEBROOT)


@app.route('/process_login', methods=['GET', 'POST'])
def process_login():
    userName = 'sec_user'
    dbPassword = keyring.get_password("Ironworks-MySQL-" + userName, userName)
    db = MySQLdb.connect(host="192.168.1.6", user=userName, passwd=dbPassword, db="secure_login")
    if request.method == 'POST':
        user = request.form['email']
        password = hashlib.sha512(request.form['p']).hexdigest()

    if login(user, password, db):
        return redirect(url_for('latestNews'))
    return render_template('index.html',
        webroot=ironworks.WEBROOT)
        #db_session.add(user)
        #flash('Thanks for registering')
        #return redirect(url_for('login'))
    #return render_template('register.html', form=form)
