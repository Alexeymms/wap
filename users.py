# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

import hashlib
from DB import *

class User():
    queryUserSelect = """
        SELECT id,username,password
        FROM users
        WHERE id = %s"""

    queryUnameSelect = """
        SELECT id,username,password
        FROM users
	WHERE username = %s"""

    queryUidSelect = """
	SELECT username
	FROM users
	WHERE id = %s"""

    def __init__(self, i_user=0):
        self.id = 0
        self.username = None
        self.password = None
        self.open(i_user)

    def open(self, i_user=0):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        if i_user == 0:
            self.id = 0
            self.username = None
            self.password = None
            self.options = None
            return

        db.execute(self.queryUserSelect, (i_user))
        row = db.fetchone()

        try:
            self.id = i_user
            self.username = row[1]
            self.password = row[2]
        except:
            self.id=0
            self.username = None
            self.password = None
            self.options = None

        self.options = User_Options(self.id)

    def get_user(self, username):
        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        db.execute(self.queryUnameSelect, (username))
        row = db.fetchone()

        try:
            self.id = row[0]
            self.username = row[1]
            self.password = row[2]
        except:
            self.id = 0
            self.username = None
            self.password = None
            self.options = None

        self.options = User_Options(self.id)

    def passcomp(self, password):
        hashpass = hashlib.sha1(self.username.lower() + password)

        print "<h1> COMPARING: {0} TO: {1}".format(hashpass.hexdigest(), self.password)

        if hashpass.hexdigest() == self.password:
            return True
        
        return False

class User_Options():
    queryOptionsSelect = """
        SELECT *
        FROM user_options
        WHERE id = %s"""

    def __init__(self, i_user):
        self.avpairs = dict()

        try:
            db = conn.cursor()
        except NameError:
            conn = DB()
            db = conn.cursor()

        if i_user == 0:
            self.avpairs = None
            return
        
        db.execute(self.queryOptionsSelect, (i_user))

        for row in db.fetchall():
            self.avpairs[row[1]] = row[2]
