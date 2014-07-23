# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import sys
import socket
import cPickle
import cStringIO
import xmlrpclib
import re
import traceback
import Localization

class Myexception(Exception):
    def __init__(self, faultCode, faultString):
        self.faultCode = faultCode
        self.faultString = faultString
        self.args = (faultCode, faultString)

class mysocket:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
        self.sock.settimeout(10)
    def connect(self, host, port=False):
        if not port:
            protocol, buf = host.split('//')
            host, port = buf.split(':')
        self.sock.connect((host, int(port)))
    def disconnect(self):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
    def mysend(self, msg, exception=False, traceback=None):

        msg = cPickle.dumps([msg,traceback])
        size = len(msg)
        self.sock.send('%8d' % size)
        self.sock.send(exception and "1" or "0")
        totalsent = 0
        while totalsent < size:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError, "socket connection broken"
            totalsent = totalsent + sent
    def myreceive(self):
        buf=''
        while len(buf) < 8:
            chunk = self.sock.recv(8 - len(buf))
            if chunk == '':
                raise RuntimeError, "socket connection broken"
            buf += chunk
        size = int(buf)
        buf = self.sock.recv(1)
        if buf != "0":
            exception = buf
        else:
            exception = False
        msg = ''
        while len(msg) < size:
            chunk = self.sock.recv(size-len(msg))
            if chunk == '':
                raise RuntimeError, "socket connection broken"
            msg = msg + chunk
        msgio = cStringIO.StringIO(msg)
        unpickler = cPickle.Unpickler(msgio)
        unpickler.find_global = None
        res = unpickler.load()

        if isinstance(res[0],Exception):
            if exception:
                raise Myexception(str(res[0]), str(res[1]))
            raise res[0]
        else:
            return res[0]


class RPCGateway(object):
    def __init__(self, host, port, protocol):

        self.protocol = protocol
        self.host = host
        self.port = port

    def get_url(self):

        """Get the url
        """
        return "%s://%s:%s/"%(self.protocol, self.host, self.port)

    def listdb(self):
        """Get the list of databases.
        """
        pass

    def login(self, db, user, password):
        pass

    def execute(self, obj, method, *args):
        pass

class RPCSession(Localization.LocalizedObject):
    def __init__(self, ctx, url):
        try:
            super(RPCSession, self).__init__(ctx, url)
        except Exception, e:
            print >> sys.stderr, e
        m = re.match('^(http[s]?://|socket://)([\w.\-]+):(\d{1,5})$', url or '')
        if not m:
            print >> sys.stderr, self.localize('invalid.url')
            ErrorDialog(self.localize('configuration.error'),
                        self.localize('invalid.url') % url or '')
            return -1
        host = m.group(2)
        port = m.group(3)
        protocol = m.group(1)
        # XMLRPClib takes socket's timeout
        # We replace it temporarily for our purposes
        # http://stackoverflow.com/questions/372365/set-timeout-for-xmlrpclib-serverproxy
        if protocol == 'http://' or protocol == 'http://': # SR: ?huh?
            self.gateway = XMLRPCGateway(host, port, 'http')
        elif protocol == 'socket://':
            self.gateway = NETRPCGateway(host, port)

    def listdb(self):
        return self.gateway.listdb()

    def login(self, db, user, password):

        if password is None:
            return -1

        uid = self.gateway.login(db, user or '', password or '')

        if uid <= 0:
            return -1

        self.uid = uid
        self.db = db
        self.password = password
        self.open = True
        return uid


    def execute(self, obj, method, *args):
        try:
            result = self.gateway.execute(obj, method, *args)
            return self.__convert(result)
        except Exception,e:
          info = reduce(lambda x, y: x+y, traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))

    def __convert(self, result):

        if isinstance(result, basestring):
            # try to convert into unicode string
            try:
                return ustr(result)
            except Exception, e:
                return result

        elif isinstance(result, list):
            return [self.__convert(val) for val in result]

        elif isinstance(result, tuple):
            return tuple([self.__convert(val) for val in result])

        elif isinstance(result, dict):
            newres = {}
            for key, val in result.items():
                newres[key] = self.__convert(val)

            return newres

        else:
            return result

class XMLRPCGateway(RPCGateway):
    """XML-RPC implementation.
    """
    def __init__(self, host, port, protocol='http'):

        super(XMLRPCGateway, self).__init__(host, port, protocol)
        global rpc_url
        rpc_url =  self.get_url() + 'xmlrpc/'

    def listdb(self):
        global rpc_url
        sock = xmlrpclib.ServerProxy(rpc_url + 'db')
        try:
            return sock.list()
        except Exception, e:
            return -1

    def login(self, db, user, password):

        global rpc_url

        sock = xmlrpclib.ServerProxy(rpc_url + 'common')

        oldtimeout = socket.getdefaulttimeout()
        socket.setdefaulttimeout(10)
        try:
            res = sock.login(db, user, password)
        except Exception, e:
            info = reduce(lambda x, y: x+y, traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))
            return -1
        finally:
            socket.setdefaulttimeout(oldtimeout)

        return res

    def execute(self, sDatabase,UID,sPassword,obj, method, *args):
        global rpc_url

        sock = xmlrpclib.ServerProxy(rpc_url + 'object')

        return sock.execute(sDatabase,UID,sPassword, obj ,method,*args)



class NETRPCGateway(RPCGateway):
    def __init__(self, host, port):

        super(NETRPCGateway, self).__init__(host, port, 'socket')

    def listdb(self):
        sock = mysocket()
        try:
            sock.connect(self.host, self.port)
            sock.mysend(('db', 'list'))
            res = sock.myreceive()
            sock.disconnect()
            return res
        except Exception, e:
            return -1

    def login(self, db, user, password):
        sock =  mysocket()
        try:
            sock.connect(self.host, self.port)
            sock.mysend(('common', 'login', db, user, password))
            res = sock.myreceive()
            sock.disconnect()
        except Exception, e:
            return -1
        return res
    def execute(self,obj, method, *args):
        sock = mysocket()
        try:
            sock.connect(self.host, self.port)
            data=(('object', 'execute',obj,method,)+args)
            sock.mysend(data)
            res=sock.myreceive()
            sock.disconnect()
            return res

        except Exception,e:
            info = reduce(lambda x, y: x+y, traceback.format_exception(sys.exc_type, sys.exc_value, sys.exc_traceback))
