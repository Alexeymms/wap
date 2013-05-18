# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

from flask import Flask, session, request, redirect, url_for, render_template
from werkzeug import secure_filename
from werkzeug.contrib.fixers import ProxyFix
import hashlib

from users import *
from card import *
from DB import *
from account import account

app = Flask(__name__)
app.register_blueprint(account)
app.jinja_env.autoescape = False

@app.route('/register')
def register():
    return "REGISTER"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user = User()
        user.get_user(request.form['username'])

        if user.id == 0:
            return "User not in database."
        
        if user.passcomp(request.form['password']) == True:
            session['username'] = request.form['username']
            session['i_user'] = user.id
            return redirect(url_for('account.account_main'))
        else:
            return "Login Incorrect"
                         
    else:
        return render_template('login.html')

@app.route('/cardauth', methods=['GET', 'POST'])
def cardauth():
    if request.method == "POST":
        card = Card()
        card.get_card(request.form['username'])

        if card.id == 0:
            return "Card not in database."

        session['card'] = card.card
        return redirect(url_for('account.account_main'))

    else:
        return reunder_template('login.html')


if __name__ == '__main__':
    app.debug = True
    app.secret_key = '2b6a57457a69559a69678bca4d5ab023'
    app.run(host='0.0.0.0', port=9001)
else:
    app.secret_key = '2b6a57457a69559a69678bca4d5ab023'
    app.wsgi_app = ProxyFix(app.wsgi_app)
