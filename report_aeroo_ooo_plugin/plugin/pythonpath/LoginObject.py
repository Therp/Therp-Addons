##########################################################################
#
#    OpenERP, Open Source Management Solution
#
#    This module (C) 2012 Therp BV (<http://therp.nl>)
#
#    Contains elements from the OpenERP Report Designer plugin
#    for OpenOffice, Copyright (C) 2004-2012 OpenERP SA 
#    (<http://openerp.com>). 
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
#
##############################################################################

import OptionsHandler
import Danny
import TinySocket
import Localization

loginstatus=False

class LoginObject(Localization.LocalizedObject):
    def getLogin(self):
        """
        Check for a valid configuration and a succesful login

        Does not return the object, but the parameters of a valid
        connection.
        """
        ConfigurationProvider = OptionsHandler.ConfigurationProvider(self.ctx)
        (url, database, login, password, options_changed) = ConfigurationProvider.get_options()
        if not (url and database and login and password):
            Danny.ErrorDialog(
                self.localize("missing"),
                self.localize("valid"))
            return False
        global loginstatus
        if not loginstatus or options_changed:
            sock = TinySocket.RPCSession(self.ctx, url)
            uid = sock.login(database, login, password)
            if not uid or uid == -1:
                Danny.ErrorDialog(
                    self.localize("refused"),
                    self.localize("valid"))
                return False
            return (url, database, uid, password)
        return False
