# wap: A minimalistic wireless billing system

# A hash table implementation based on the MurmurHash 2.0 hash function

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

from flask import Blueprint, session, request, redirect, url_for, render_template
from werkzeug import secure_filename
from werkzeug.contrib.fixers import ProxyFix

from DB import *
from card import *
from users import *
from ledger import *
from config import *

Config = Config()

account = Blueprint('account', __name__)

@account.route('/account')
def account_main():
    if session['card']:
        card = Card()
        card.get_card(session['card'])
        
        ledger = Ledger()
        ledger.bycard(card.id)
        
        balance = ledger.get_balance()

        return render_template("account.html",
                               username=card.card,
                               password=card.card,
                               ledger=ledger,
                               balance=balance,
                               zdconfig=Config.zonedirector)
