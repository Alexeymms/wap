# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

from DB import *

class Product():
    queryProductByCard = """
        SELECT p.id, p.name, p.description, p.price, p.activation, p.fee, p.day
        FROM products AS p, cards AS c
        WHERE c.id = %s"""

    queryProductByUser = """
        SELECT p.id, p.name, p.description, p.price, p.activation, p.fee, p.day
        FROM products AS p, users AS u
        WHERE u.id = %s"""

    def __init__(self):
        self.id = 0
        self.name = None
        self.description = None
        self.price = 0
        self.activation = 0
        self.fee = 0
        self.day = 0

    def user(self, i_user=0):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryProductByUser, (i_user))
        rows = db.fetchall()

        self.id          = rows[0][0]
        self.name        = rows[0][1]
        self.description = rows[0][2]
        self.price       = rows[0][3]
        self.activation  = rows[0][4]
        self.fee         = rows[0][5]
        self.day         = rows[0][6]

    def card(self, i_card=0):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryProductByCard, (i_card))
        rows = db.fetchall()

        self.id          = rows[0][0]
        self.name        = rows[0][1]
        self.description = rows[0][2]
        self.price       = rows[0][3]
        self.activation  = rows[0][4]
        self.fee         = rows[0][5]
        self.day         = rows[0][6]
