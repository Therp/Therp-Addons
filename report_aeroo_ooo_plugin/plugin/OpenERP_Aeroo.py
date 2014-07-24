# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012-2014 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

import os
import sys
import unohelper
import base64
import tempfile
import traceback
from com.sun.star.task import XJobExecutor

try:
    import Danny
except ImportError:
    #enable to run without extension context
    sys.path.append(os.path.join(
        os.path.dirname(__file__),
        'pythonpath',
    ))
    import Danny
import TinySocket
import FileUtils
import Localization
import LoginObject


class Merge(Localization.LocalizedObject, XJobExecutor):
    """
    Send the current open document to the OpenERP server
    and trigger an Aeroo report on resources in the
    stored selection. Merge the documents into one, separated
    by newlines on the OpenOffice side and open the document
    in the user's window.
    """

    def __init__(self, ctx):
        super(Merge, self).__init__(ctx)
        self.ctx = ctx
        self.module = "OpenERP_Aeroo"
        self.version = "0.1"

    def trigger(self, args):
        login = LoginObject.LoginObject(self.ctx).getLogin()
        if not login:
            exit(1)
        (url, database, uid, password) = login
        self.sock = TinySocket.RPCSession(self.ctx, url)
        Desktop = Danny.getDesktop()
        current = Desktop.getCurrentComponent()
        if not current.hasLocation():
            tempFile = tempfile.mkstemp('.odt')
            os.close(tempFile[0])
            tempURL = Danny.convertToURL(tempFile[1])
            current.storeAsURL(
                tempURL,
                Danny.Array(
                    Danny.makePropertyValue(
                        "MediaType",
                        "application/vnd.oasis.opendocument.text"))
                )
        current.store()

        dialog = self.ctx.getServiceManager()\
            .createInstanceWithContext(
                "com.sun.star.awt.DialogProvider", self.ctx)\
            .createDialog(
                "vnd.sun.star.extension://org.odoo.report_aeroo_ooo_plugin/"
                "dialogs/FilterChooser.xdl")

        listbox = dialog.getControl('filter')
        filters = self.sock.execute(
            database, uid, password, 'ir.filters', 'get_libreoffice_filters')
        listbox.addItems(tuple(n for i, n in filters), 0)
        listbox.setText(listbox.getItem(0))

        filter_id = None
        if dialog.execute():
            filter_id = None
            filters = [i for i, n in filters if n == listbox.getText()]
            if filters:
                filter_id = filters[0]
            else:
                dialog.dispose()
                return
        dialog.dispose()

        data = FileUtils.read_data_from_file(
            FileUtils.get_absolute_file_path(
                current.getURL()[7:]
                )
            )
        res = self.sock.execute(
            database,
            uid,
            password,
            'instant.aeroo',
            'create_report',
            base64.encodestring(data),
            filter_id
            )
        if res:
            if res[0]:
                # Combine files, based on
                # Russell Philip's OOO Macros
                # http://sourceforge.net/projects/ooomacros/files/ (GPL)
                tempFile = tempfile.mkstemp('.odt')
                os.close(tempFile[0])
                filename = tempFile[1]
                FileUtils.write_data_to_file(filename,
                                             base64.decodestring(res[0]))
                Desktop.loadComponentFromURL(
                    Danny.convertToURL(filename), "_blank", 0, ())
            else:
                # Second arg *may* contain a warning or error message
                Danny.ErrorDialog(self.localize("error"), "%s" % res[1])
        else:
            Danny.ErrorDialog(self.localize("error"),
                              self.localize("not.create"))

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    Merge,
    "org.odoo.report_aeroo_ooo_plugin.merge",
    ("com.sun.star.task.Job",),)


class About(Localization.LocalizedObject, XJobExecutor):
    def __init__(self, ctx):
        super(About, self).__init__(ctx)
        self.module = "OpenERP_Aeroo"
        self.version = "0.1"
        self.win = Danny.DBModalDialog(
            60, 50, 200, 215,
            self.localize("about"))

    def trigger(self, args):
        fdBigFont = Danny.createUnoStruct("com.sun.star.awt.FontDescriptor")
        fdBigFont.Width = 20
        fdBigFont.Height = 25
        fdBigFont.Weight = 120
        fdBigFont.Family = 3

        oLabelProdDesc = self.win.addFixedText("lblProdDesc", 3, 30, 196, 175)
        oLabelProdDesc.Model.TextColor = 1
        fdBigFont.Width = 10
        fdBigFont.Height = 11
        fdBigFont.Weight = 76
        oLabelProdDesc.Model.FontDescriptor = fdBigFont
        oLabelProdDesc.Model.Align = 1
        oLabelProdDesc.Model.FontRelief = 1
        oLabelProdDesc.Model.MultiLine = True
        oLabelProdDesc.Text = self.localize("content")

        self.win.doModalDialog("", None)

g_ImplementationHelper.addImplementation(
    About,
    "org.odoo.report_aeroo_ooo_plugin.about",
    ("com.sun.star.task.Job",),)

if __name__ == "__main__":
# from https://wiki.openoffice.org/wiki/UNO_component_packaging#
# Python_component_testing
    import os
    import uno

    # Start OpenOffice.org, listen for connections and open testing document
    os.system("lowriter '--accept=socket,host=localhost,port=2002;urp;' &")

    # Get local context info
    localContext = uno.getComponentContext()
    resolver = localContext.ServiceManager.createInstanceWithContext(
        "com.sun.star.bridge.UnoUrlResolver", localContext)

    ctx = None

    # Wait until the OO.o starts and connection is established
    while ctx is None:
        try:
            ctx = resolver.resolve(
                "uno:socket,host=localhost,port=2002;urp;"
                "StarOffice.ComponentContext")
        except:
            pass

    # Trigger our job
    merge = Merge(ctx)
