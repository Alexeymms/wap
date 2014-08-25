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

import ldap

from config import *
from users import *

#
# There is currently a problem with this module.
#
# When imported by FreeRADIUS it's throwing strange error messages.
# To fix this you *MUST* build python2 with UCS2 instead of UCS4
#
class Ldap(User):
    ''' This class overrides the DB-driven User() object.  It does a few
    things differently.  Chiefly:
    
    1) We never store the password.
    2) We don't bother to authenticate the Username until the first
       call to passcomp() '''

    def __init__(self, i_user=0):
        User.__init__(self, 0)
        self.config = Config()        
        self.ldap = ldap.open(self.config.ldap['server'],
                              port=self.config.ldap['port'])
        self.ldap.protocol_version = ldap.VERSION3
        self.ldap.set_option(ldap.OPT_REFERRALS, 0)

    def get_user(self, username):
        ''' We can't really return an authenticated user just yet.
        We must first attempt a bind with passcomp.  So for now, we
        simply take the client's word at their username'''

        self.username = username

    def passcomp(self, password):
        ''' In order to authenticate the user, we simply make an
        attempt to bind it to the LDAP server'''
        
        try:
            self.ldap.simple_bind_s(self.gendn(), password)
        except ldap.INVALID_CREDENTIALS:
            return False

        return True

    def gendn(self):
        return '{2}={0},{1}'.format(self.username, 
                                    self.config.ldap['basedn'],
                                    self.config.ldap['searchkey'])

