# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

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
