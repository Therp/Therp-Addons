# # -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012 Therp BV (<http://therp.nl>).
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

from osv import fields, osv

class account_invoice(osv.osv):
    _inherit = 'account.invoice'
    _columns = {
        'report_background_id': fields.many2one(
            'report.background', 'Report background'),
        }

    def _auto_init(self, cr, context=None):
        res = super(account_invoice, self)._auto_init(cr, context=context)
        cr.execute("""
            SELECT COUNT(*) FROM ir_translation
            WHERE type = 'report' AND name = 'account.invoice.background'
        """)
        if not cr.fetchone()[0]:
            # Copy translations from the original invoice report
            # to the copy that this module adds
            cr.execute(
                """
                INSERT INTO ir_translation (lang,src,name,type,value)
                SELECT lang, src, %s, 'report',value
                FROM ir_translation WHERE type = 'report' AND name = %s;
                """, ('account.invoice.background', 'account.invoice')
                )
        return res
