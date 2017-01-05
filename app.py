"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

This file creates your application.
"""

import os
import pg
from flask import Flask, render_template, request, redirect, url_for

import sys

reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

DBUSER=os.environ.get('DBUSER', True)
DBPASS=os.environ.get('DBPASS', True)
DBHOST=os.environ.get('DBHOST', True)
DBNAME=os.environ.get('DBNAME', True)

###
# Routing for your application.
###
db=pg.DB(host=DBHOST, user=DBUSER, passwd=DBPASS, dbname=DBNAME)

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return 'Logged Out!'

@app.route('/new_user', methods=['GET'])
def new_user():
    return render_template("new_user.html")

@app.route('/new_user_submit', methods=['GET', 'POST'])
def new_user_submit():
    username=request.form.get('username')
    password=request.form.get('password')
    password1=request.form.get('password1')
    if password == password1:
        db.insert('users', username = username, password = password)
        return redirect('/')
    else:
        return redirect("/new_user")

@app.route('/submit_login', methods=['POST'])
def submit_login():
    username = request.form.get('username')
    password = request.form.get('password')
    query = db.query("select * from users where username = '%s'" % username)
    result_list = query.namedresult()
    if len(result_list) > 0:
        user = result_list[0]
        if user.password == password:
            session['username'] = user.username
            session['logged in'] = True
            return render_template("sucess.html")
        else:
            return redirect('/')
    else:
        return render_template("login_fail.html")
