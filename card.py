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

class Card():
    queryCardSelect = """
        SELECT id,card,balance
        FROM cards
	WHERE card = %s"""

    queryCidSelect = """
	SELECT id,card,balance
	FROM cards
	WHERE id = %s"""

    def __init__(self, i_card=0):
        self.id = 0
        self.card = None
        self.balance = 0.00
        self.options = None
        self.open(i_card)

    def open(self, i_card=0):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        if i_card == 0:
            self.id = 0
            self.card = None
            self.balance = 0.00
            self.options = None;
            return

        db.execute(self.queryCidSelect, (i_card))
        row = db.fetchone()
        
        try:
            self.id = row[0]
            self.card = row[1]
            self.balance = row[2]
        except:
            self.id = 0
            self.card = None
            self.balance = 0.00
            self.options = None;

        self.options = Card_Options(self.id)

    def get_card(self, card):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryCardSelect, (card))
        row = db.fetchone()

        try:
            self.id = row[0]
            self.card = row[1]
            self.balance = row[2]
        except:
            self.id = 0
            self.card = None
            self.balance = 0.00
            self.options = None;

        self.options = Card_Options(self.id)


class Card_Options():
    queryOptionsSelect = """
        SELECT *
        FROM card_options
        WHERE id = %s"""

    def __init__(self, i_card):
        self.avpairs = dict()

        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        if i_card == 0:
            self.avpairs = None
            return
        
        db.execute(self.queryOptionsSelect, (i_card))

        for row in db.fetchall():
            self.avpairs[row[1]] = row[2]
