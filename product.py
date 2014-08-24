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
