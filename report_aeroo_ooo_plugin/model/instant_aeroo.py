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
from openerp.osv import osv
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval
from openerp.report.report_sxw import rml_parse
from openerp.addons.report_aeroo.report_aeroo import Aeroo_report
from openerp.addons.report_aeroo.report_aeroo import AerooPrint


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
    report_name = ''
    id = []

    def __init__(self, file_data):
        #self.id = 0
        self.report_sxw_content = file_data
        # TODO: detect file_data mime type
        # and adjust in_format accordingly
        self.in_format = 'oo-odt'


class Aeroo_report_instant(Aeroo_report):

    def __init__(self, cr, table):
        self.name = 'report.odt.instantaeroo'
        self.name2 = 'odt'
        self.oo_subreports = []
        self.epl_images = []
        self.counters = {}
        self.table = table
        self.parser = rml_parse
        self.active_prints = {False: AerooPrint()}


class instant_aeroo(osv.TransientModel):
    _name = 'instant.aeroo'
    """ Wrapper for Aeroo_instant_report, as exposed through xml-rpc """

    def create_report(self, cr, uid, file_data, filter_id, context=None):
        """
        Return a tuple (list_of_docs, type)
        """
        if context is None:
            context = {}

        saved_filter = self.pool['ir.filters'].browse(cr, uid, filter_id,
                                                      context=context)
        ids = self.pool[saved_filter.model_id].search(
            cr, uid,
            safe_eval(saved_filter.domain),
            context=safe_eval(saved_filter.context))

        if not ids:
            return (False, _("User's selection does not contain any items."))

        data = {
            'report_type': 'aeroo',
            'model': saved_filter.model_id
        }
        ctx = context.copy()
        ctx['active_model'] = saved_filter.model_id

        try:
            report = Aeroo_report_instant(cr, saved_filter.model_id)
            report_xml = report_xml_duck(file_data)
            res = report.create_aeroo_report(
                cr, uid, ids, data, report_xml, context=context)
            return (base64.encodestring(res[0]), res[1])
        except ValueError, e:
            return (False, unicode(e))
