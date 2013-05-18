# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

##
# This imports CSV files or something
##
from DB import *

conn = DB()

if __name__ == '__main__':
    db = conn.cursor()
    f = open("DATA-BATCH-1-20-APR-2013.csv", "r")
    for line in f:
        card = line.rstrip()
        print card
        Number, Value = card.split(",")
        
        db.execute("INSERT INTO cards (card, balance) VALUES (%s, %s)", (Number, Value))
        i_card = db.lastrowid
        db.execute("INSERT INTO ledger (i_card, type, amount, reason) VALUES (%s, %s, %s, %s)", (i_card, "Credit", Value, "Card Created"))
