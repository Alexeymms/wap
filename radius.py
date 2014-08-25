#!/usr/bin/env python
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

from nas import *
from users import *
from users_ldap import *
from card import *
from ledger import *
from product import *
from DB import *
from config import *

conn = None
Config = Config()

def instantiate(p):
    conn = DB()

def authorize(p):
    #
    # We need to initialize some variables to avoid throwing exceptions later
    #
    Username = None
    Password = None
    NasIdentifier = None
    NasIPAddress = None
    ServiceType = None
    attribs = (('Class', 'Internet'),)

    #
    # Loop through the NAS-supplied attributes to figure some things out
    #
    for (Key, Value) in p:
        Value = re.sub(r'^"|"$', '', Value)
        print "{0} = {1}".format(Key, Value)

        if Key == "User-Name":
            Username = Value

        if Key == "User-Password":
            Password = Value

        if Key == "Service-Type":
            ServiceType = Value

        if Key == "NAS-Identifier":
            NasIdentifier = Value
            
        if Key == "NAS-IP-Address":
            NasIPAddress = None;

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
            # Add card-specific attributes to the Access-Accept packet.
            for key in card.options.avpairs:
                attribs = attribs + ((key, card.options.avpairs[key]),)
        else:
            return(radiusd.RLM_MODULE_REJECT)

    #
    # LDAP-Enabled login
    #
    elif Config.ldap['enabled']:
        #
        # We need to set this here because the NAS won't do it
        # and we cannot currently keep accounting information
        # for ldap-enabled clients
        #
        ServiceType = "Authenticate-Only"

        try:
            user = Ldap()
            user.get_user(Username)
        except:
            return(radiusd.RLM_MODULE_FAIL)    
            
        if not user.passcomp(Password):
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
            # Add user-specific attributes to the Access-Accept packet.
            for key in user.options.avpairs:
                attribs = attribs + ((key, user.options.avpairs[key]),)
        else:
            return(radiusd.RLM_MODULE_REJECT)

    #
    # Add NAS-specific attributes to the Access-Accept packet.
    #
    nas = Nas()
    if NasIdentifier:
        nas.get_nas(NasIdentifier)
        try:
            for key in nas.options.avpairs:
                attribs = attribs + ((key, nas.options.avpairs[key]),)
        except TypeError:
            pass

    #
    # If the NAS isn't specifically requesting Service-Type=Authenticate-Only,
    # then we need to check the balance before we send off an Access-Accept
    #
    if ServiceType != "Authenticate-Only":
        Balance = ledger.get_balance()
        if Balance >= 0.01:
            pass
        else:
            return(radiusd.RLM_MODULE_REJECT)

    return(radiusd.RLM_MODULE_UPDATED, attribs, (('Auth-Type', 'Accept'),))
    

def preacct(p):
    return radiusd.RLM_MODULE_OK

def accounting(p):
    try:
        db = conn.cursor()
    except NameError:
        conn = DB()
        db = conn.cursor()

    #
    # No accounting for LDAP (yet)
    #
    if Config.ldap['enabled']:
        return radiusd.RLM_MODULE_FAIL

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

