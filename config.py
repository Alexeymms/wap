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

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

class Config():
    def __init__(self, configfile='./wap.conf'):
        self.config = SafeConfigParser()
        self.config.read(configfile)
        self.configfile = configfile
        self.database = dict()
        self.zonedirector = dict()
        self.ldap = dict()

        if self.config.has_section('database'):
            try:
                self.database['user'] = self.config.get('database', 'user')
                self.database['pass'] = self.config.get('database', 'pass')
                self.database['host'] = self.config.get('database', 'host')
                self.database['db'] = self.config.get('database', 'db')   
            except:
                self.database['user'] = None
                self.database['host'] = None
                self.database['pass'] = None
                self.database['db'] = None

        if self.config.has_section('zonedirector'):
            try:
                self.zonedirector['login'] = self.config.get('zonedirector', 'login')
                self.zonedirector['logout'] = self.config.get('zonedirector', 'logout')
            except:
                self.zonedirector['login'] = None
                self.zonedirector['logout'] = None

        if self.config.has_section('ldap'):
            try:
                self.ldap['enabled'] = self.config.get('ldap', 'enabled')
                self.ldap['basedn'] = self.config.get('ldap', 'basedn')
                self.ldap['binddn'] = self.config.get('ldap', 'binddn')
                self.ldap['bindpw'] = self.config.get('ldap', 'bindpw')
                self.ldap['server'] = self.config.get('ldap', 'server')
                self.ldap['port'] = int(self.config.get('ldap', 'port'))
                self.ldap['bindonauth'] = self.config.get('ldap', 'bindonauth')
                self.ldap['searchkey'] = self.config.get('ldap', 'searchkey')
            except:
                self.ldap = dict()
                self.ldap['enabled'] = False

            self.ldap['enabled'] = self.translateliteral(self.ldap['enabled'])
            self.ldap['binddn'] = self.translateliteral(self.ldap['enabled'])
            self.ldap['bindpw'] = self.translateliteral(self.ldap['enabled'])
            self.ldap['bindonauth'] = self.translateliteral(self.ldap['bindonauth'])

    def translateliteral(self, literal='None'):
        if literal == 'False':
            return False;
        if literal == 'True':
            return True;
        if literal == 'None':
            return None;

