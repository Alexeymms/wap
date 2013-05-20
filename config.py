# wap: A minimalistic wireless billing system

# Copyright(C) 2013 Global Reach Communications, Inc.
# All Rights Reserved.

# You have obtained a development version of this software in its source format.
# You may not modify, redistribute or re-use this software under any circumstances,
# including (but not limited to): selling, sublicensing, transferring owership,
# creating derivative works, copying or reinstalling.  For more information, please
# contact licensing@globalreachcomm.com

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError

class Config():
    def __init__(self, configfile='./wap.conf'):
        self.config = SafeConfigParser()
        self.config.read(configfile)
        self.configfile = configfile
        self.database = dict()
        self.zonedirector = dict()

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
