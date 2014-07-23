# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (c) 2012 Therp BV (<http://therp.nl>)
# 
#    Heavily based on and to be used with the Aeroo reports modules
#        which are
#        Copyright (c) 2009-2011 Alistek Ltd (http://www.alistek.com)
#        Copyright (C) 2009  Domsense s.r.l.                                   
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
"""
Usage scenario:

The user has a template opened in his OpenOffice word processor. He connects
 to the OpenERP server. The template is uploaded and applied to the contents
of his stored selection. The user receives back from the OpenERP server a
single merged document.

"""

import base64
from osv import osv
from report.report_sxw import rml_parse
from report_aeroo.report_aeroo import Aeroo_report
import pooler

class report_xml_duck(object):
    attachment = False
    attachment_use = False
    process_sep = False
    report_type = 'aeroo'
    styles_mode = 'default'
    tml_source = 'database'
    preload_mode = False
    fallback_false = True
    content_fname = False
    id = []

    def __init__(self, file_data):
        #self.id = 0
        self.report_sxw_content = file_data
        # TODO: detect file_data mime type
        # and adjust in_format accordingly
        self.in_format = 'oo-odt'

class Aeroo_report_instant(Aeroo_report):

    def __init__(self, cr, table):
#        super(Aeroo_instant_report, self).__init__(name, table, rml, parser, header, store)
#        self.logger("registering %s (%s)" % (name, table), netsvc.LOG_INFO)
        self.name = 'report.odt.instantaeroo'
        self.name2 = 'odt'
        self.oo_subreports = []
        self.epl_images = []
        self.counters = {}
        self.table = table
        self.parser = rml_parse

class instant_aeroo(osv.TransientModel):
    _name = 'instant.aeroo'
    """ Wrapper for Aeroo_instant_report, 
    as exposed through xml-rpc
    """

    def create_report(self, cr, uid, file_data, context=None):
        """
        Return a tuple (list_of_docs, type)
        """
        if context is None:
            context = {}
       
        store = self.pool.get('saved_selection.selection').get(
            cr, uid, context)
        if not store:
            return (False, "No saved selection defined for this user.")

        # TODO: do a check against the template model?
        (model, ids) = store
        if not ids:
            return (False, "User's selection does not contain any items.")

        data = {
            'report_type': 'aeroo',
            'model': model
        }
        context['active_model'] = model
                
        try:
            report = Aeroo_report_instant(cr, model)
            report_xml = report_xml_duck(file_data)
            to_return = [[], False]
            for res_id in ids:
                res = report.create_aeroo_report(
                    cr, uid, [res_id], data, report_xml, context=context)
                if res and res[0]:
                    to_return[0].append(base64.encodestring(res[0]))
                    to_return[1] = res[1]
        except Exception, e:
            to_return = (False, unicode(e))
        return to_return
