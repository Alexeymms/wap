# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

from DB import *

class Nas():
    queryNasSelect = """
        SELECT id,identifier,description
        FROM nas
	WHERE identifier = %s"""

    queryNidSelect = """
        SELECT id,identifier,description
	FROM nas
	WHERE id = %s"""

    def __init__(self, i_nas=0):
        self.id = 0
        self.identifier = None
        self.description = None
        self.options = None
        self.open(i_nas)

    def open(self, i_nas=0):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        if i_nas == 0:
            self.id = 0
            self.identifier = None
            self.description = None
            self.options = None;
            return

        db.execute(self.queryNidSelect, (i_nas))
        row = db.fetchone()
        
        try:
            self.id = row[0]
            self.identifier = row[1]
            self.description = row[2]
        except:
            self.id = 0
            self.identifier = None
            self.description = None
            self.options = None;

        self.options = Nas_Options(self.id)

    def get_nas(self, identifier):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryNasSelect, (identifier))
        row = db.fetchone()

        try:
            self.id = row[0]
            self.identifier = row[1]
            self.description = row[2]
        except:
            self.id = 0
            self.identifier = None
            self.description = None
            self.options = None

        self.options = Nas_Options(self.id)


class Nas_Options():
    queryOptionsSelect = """
        SELECT *
        FROM nas_options
        WHERE id = %s"""

    def __init__(self, i_nas):
        self.avpairs = dict()

        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        if i_nas == 0:
            self.avpairs = None
            return
        
        db.execute(self.queryOptionsSelect, (i_nas))

        for row in db.fetchall():
            self.avpairs[row[1]] = row[2]

