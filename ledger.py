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
