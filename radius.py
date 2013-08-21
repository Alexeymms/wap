#!/usr/bin/env python
# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

# RLM_MODULE_REJECT = 0
# RLM_MODULE_FAIL = 1
# RLM_MODULE_OK = 2
# RLM_MODULE_HANDLED = 3
# RLM_MODULE_INVALID = 4
# RLM_MODULE_USERLOCK = 5
# RLM_MODULE_NOTFOUND = 6
# RLM_MODULE_NOOP = 7	
# RLM_MODULE_UPDATED = 8
# RLM_MODULE_NUMCODES = 9
import radiusd
import re

from users import *
from card import *
from ledger import *
from product import *
from DB import *

conn = None

def instantiate(p):
    conn = DB()

def authorize(p):
    for (Key, Value) in p:
        Value = re.sub(r'^"|"$', '', Value)
        print "{0} = {1}".format(Key, Value)

        if Key == "User-Name":
            Username = Value

        if Key == "User-Password":
            Password = Value

    #
    # Someone's trying to log in with a card
    #
    if Username == Password:
        try:
            card = Card()
            card.get_card(Username)
            ledger = Ledger()
            ledger.bycard(card.id)
        except:
            return(radiusd.RLM_MODULE_FAIL)

        if card.id > 0:
            pass
        else:
            return(radiusd.RLM_MODULE_REJECT)

    #
    # Logging in with username and password
    #
    else:
        try:
            user = User()
            user.get_user(Username)
            ledger = Ledger()
            ledger.byuser(user.id)
        except:
            return(radiusd.RLM_MODULE_FAIL)
            
        if user.passcomp(Password) == True:
            pass
        else:
            return(radiusd.RLM_MODULE_REJECT)

    #
    # Finally, check the balance
    #
    Balance = ledger.get_balance()
    if Balance >= 0.01:
        return(radiusd.RLM_MODULE_UPDATED, 
               (('Class', 'Internet')
                ('Framed-Route', 's1d1'),
                ('Framed-Pool', '41.79.196.1')),
               (('Auth-Type', 'python')))
    else:
            return(radiusd.RLM_MODULE_REJECT)

def preacct(p):
    return radiusd.RLM_MODULE_OK

def accounting(p):
    try:
        db = conn.cursor()
    except NameError:
        conn = DB()
        db = conn.cursor()

    #
    # Let's figure out what the AP is trying to tell us
    #
    AVPairs = dict()
    for (Key, Value) in p:
        Value = re.sub(r'^"|"$', '', Value)
        print "{0} = {1}".format(Key, Value)
        AVPairs[Key] = Value

    #
    # First thing we need to determine is whether the AP is talking
    # about a card or an authenticated user.
    #
    u = User()
    u.get_user(AVPairs['User-Name'])
    c = Card()
    c.get_card(AVPairs['User-Name'])
    p = Product()

    if u.id > 0:
        Type = 'user'
        p.user(u.id)
    elif c.id > 0:
        Type = 'card'
        p.card(c.id)
    else:
        return radiusd.RLM_MODULE_FAIL

    #
    # Process packet
    #
    if AVPairs['Acct-Status-Type'] == 'Interim-Update':
        l = Ledger()
        Bytes = int(AVPairs['Acct-Output-Octets']) + int(AVPairs['Acct-Input-Octets'])
        Amount = (Bytes / 1048576) * p.price
        db.execute('UPDATE ledger SET reason = %s, amount = %s WHERE session = %s',
                   ('Data Usage: {0} Bytes'.format(Bytes),
                    Amount, AVPairs['Acct-Multi-Session-Id']))

    elif AVPairs['Acct-Status-Type'] == 'Start':
        l = Ledger()
        if Type == 'card':
            db.execute("INSERT INTO ledger (i_card, type, amount, reason, session) VALUES (%s, %s, %s, %s, %s)", (c.id, 'Debit', 0.00, 'Session Login: {0}'.format(AVPairs['Acct-Multi-Session-Id']), AVPairs['Acct-Multi-Session-Id'])) 
        elif Type == 'user':
            db.execute("INSERT INTO ledger (i_user, type, amount, reason, session) VALUES (%s, %s, %s, %s, %s)", (u.id, 'Debit', 0.00, 'Session Login: {0}'.format(AVPairs['Acct-Multi-Session-Id']), AVPairs['Acct-Multi-Session-Id'])) 
        else:
            return radiusd.RLM_MODULE_FAIL

    elif AVPairs['Acct-Status-Type'] == 'Stop':
        l = Ledger()
        Bytes = int(AVPairs['Acct-Output-Octets']) + int(AVPairs['Acct-Input-Octets'])
        Amount = (Bytes / 1048576) * p.price
        db.execute('UPDATE ledger SET reason = %s, amount = %s WHERE session = %s',
                   ('Data Usage: {0} Bytes'.format(Bytes),
                    Amount, AVPairs['Acct-Multi-Session-Id']))

    else:
        return radiusd.RLM_MODULE_FAIL

    # 
    # If we get here we've successfully processed an accounting packet.  Now
    # we need to know what the new balance is on the account.
    # 
    if Type == 'card':

        #
        # TODO: There really needs to be a mechanism to do this inside of
        #       the Ledger() class.
        #
        l.entries = list()
        l.bycard(c.id)
    else:
        l.entries = list()
        l.byuser(u.id)

    Balance = l.get_balance()

    #
    # Return to the client.  Either A) RLM_MODULE_OK if the session can contine
    # or we send RLM_MODULE_UPDATED with Termination-Action=RADIUS-Request if
    # the user has run out of credit and we want to kill the session
    #
    if Balance >= 0.01:
        return radiusd.RLM_MODULE_OK
    else:
        return(radiusd.RLM_MODULE_UPDATED,
               (('Termination-Action', 'RADIUS-Request')))

def pre_proxy(p):
    return radiusd.RLM_MODULE_OK

def post_proxy(p):
    return radiusd.RLM_MODULE_OK

def post_auth(p):
    return radiusd.RLM_MODULE_OK

def recv_coa(p):
    return radiusd.RLM_MODULE_OK

def send_coa(p):
    return radiusd.RLM_MODULE_OK

def detach():
    return radiusd.RLM_MODULE_OK

