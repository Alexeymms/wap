# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

from DB import *
from users import *

class Ledger():
    queryLedgerByCard = """
        SELECT type, amount, reason, i_agent, session, ts
        FROM ledger
        WHERE i_card = %s"""

    queryLedgerByUser = """
        SELECT type, amount, reason, i_agent, session, ts
        FROM ledger
        WHERE i_user = %s"""

    queryLedgerBySession = """
        SELECT type, amount, reason, i_agent, session, ts
        FROM ledger
        WHERE session = %s"""

    def __init__(self):
        self.entries = list()

    def bycard(self, i_card):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryLedgerByCard, (i_card))
        rows = db.fetchall()

        for row in rows:
            Entry = dict()
            Entry['type'] = row[0]
            Entry['amount'] = row[1]
            Entry['reason'] = row[2]
            Entry['agent'] = User(row[3])
            Entry['session'] = row[4]
            Entry['ts'] = row[5]

            self.entries.append(Entry)
            
    def byuser(self, i_user):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryLedgerByUser, (i_user))
        rows = db.fetchall()

        for row in rows:
            Entry = dict()
            Entry['type'] = row[0]
            Entry['amount'] = row[1]
            Entry['reason'] = row[2]
            Entry['agent'] = User(row[3])
            Entry['session'] = row[4]
            Entry['ts'] = row[5]

            self.entries.append(Entry)

    def lastentrybysession(self, session):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryLedgerEntryBySession, (session))
        rows = db.fetchall()

        for row in rows:
            Entry = dict()
            Entry['type'] = row[0]
            Entry['amount'] = row[1]
            Entry['reason'] = row[2]
            Entry['agent'] = User(row[3])
            Entry['session'] = row[4]
            Entry['ts'] = row[5]

        return Entry

    def bysession(self, session):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryLedgerEntryBySession, (session))
        rows = db.fetchall()

        for row in rows:
            Entry = dict()
            Entry['type'] = row[0]
            Entry['amount'] = row[1]
            Entry['reason'] = row[2]
            Entry['agent'] = User(row[3])
            Entry['session'] = row[4]
            Entry['ts'] = row[5]

            self.entries.append(Entry)

    def get_balance(self):

        Balance = 0
        for Entry in self.entries:
            if Entry['type'] == 'Credit':
                Balance = Balance + Entry['amount']
            if Entry['type'] == 'Debit':
                Balance = Balance - Entry['amount']

        return Balance
