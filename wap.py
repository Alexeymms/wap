# wap: A minimalistic wireless billing system

# Copyright (c) 2013, 2014 Daniel Corbe
# All rights reserved.

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:

# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the authors, copyright holders or the contributors
#    may be used to endorese or promote products derived from this software
#    without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS, AUTHORS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL
# THE COPYRIGHT HOLDERS, AUTHORS OR CONTRIBUTORS BE HELD LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
# GOODS OR SERVICES; LOSS OF USE, DATA, COPYRIGHT ENFRINGEMENT, LOSS
# OF PROFITS, REVENUE, OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
# OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

from flask import Flask, session, request, redirect, url_for, render_template
from werkzeug import secure_filename
from werkzeug.contrib.fixers import ProxyFix
import hashlib

from users import *
from users_ldap import *
from card import *
from DB import *
from config import *

from account import account

app = Flask(__name__)
app.register_blueprint(account)
app.jinja_env.autoescape = False
Config = Config()

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        pass
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        if Config.ldap['enabled']:
            user = Ldap()
        else:
            user = User()

        user.get_user(request.form['username'])

        if user.username == None:
            return "User not in database."
        
        if user.passcomp(request.form['password']) == True:
            session['username'] = request.form['username']
            session['i_user'] = user.id
            session['password'] = request.form['password']
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
