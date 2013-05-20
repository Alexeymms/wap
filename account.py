# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

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
