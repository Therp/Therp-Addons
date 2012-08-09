# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (c) 2012 Therp BV (<http://therp.nl>)
# 
#    Thanks to the contributors of Stackoverflow refered to below.
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

import os, glob, base64
import zipfile
from StringIO import StringIO
from osv import osv, fields
from addons import get_module_resource

class GetPlugin(osv.TransientModel):
    _name = 'report.aeroo.get_plugin'

    def get_plugin_zipfile(self, cr, uid, context=None):

        def addFolderToZip(myZipFile, folder, path):
            # http://stackoverflow.com/questions/458436/adding-folders-to-a-zip-file-using-python/459419#459419
            folder = folder.encode('ascii') #convert path to ascii for ZipFile Method
            for file in glob.glob(folder + "/*"):
                relpath = os.path.join(path, os.path.basename(file))
                print relpath
                if os.path.isfile(file):
                    myZipFile.write(file, relpath, zipfile.ZIP_DEFLATED)
                elif os.path.isdir(file):
                    addFolderToZip(myZipFile, file, relpath)

        # http://stackoverflow.com/questions/3610221/how-to-create-an-in-memory-zip-file-with-directories-without-touching-the-disk
        inMemoryOutputFile = StringIO()
        zipFile = zipfile.ZipFile(inMemoryOutputFile, 'w') 
        addFolderToZip(
            zipFile, get_module_resource('report_aeroo_ooo_plugin', 'plugin'), '')
        zipFile.close()
        inMemoryOutputFile.seek(0)
        return base64.encodestring(inMemoryOutputFile.getvalue())
    
    _columns = {
        'name': fields.char(
            'Filename', size=128, readonly=True),
        'plugin_file': fields.binary(
            'OpenOffice.org/LibreOffice Extension',
            readonly=True),
        }

    _defaults = {
        'plugin_file': get_plugin_zipfile,
        'name': 'OpenERP_Aeroo.oxt',
        }
