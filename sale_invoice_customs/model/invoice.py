# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
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
from lxml import etree
from openerp.osv import fields, orm


class account_invoice(orm.Model):
    _inherit = 'account.invoice'

    _columns = {
        'active': fields.boolean("Active"),
    }

    _defaults = {
        'active': True,
    }

    def _check_valid_customs(self, cr, uid, ids, context=None):
        this = self.browse(cr, uid, ids, context=context)
        stock_pickings = self.pool.get('stock.picking')
        for data in this:
            if not data.active and not stock_pickings.search(
                    cr, uid, [
                        ('customs_invoice_id', '=', data.id)
                    ]):
                return False
        return True

    _constraints = [(_check_valid_customs,
                    'All custom invoices must be tagged False', ['active']),
                    ]

    def fields_view_get(
            self, cr, uid, view_id=None, view_type='form', context=None,
            toolbar=False, submenu=False):
        """ Disallow the user to create an invoice
        from the customs invoices menu"""
        res = super(account_invoice, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=submenu)

        if (view_type in ['tree', 'form'] and
                not (context or {}).get('active', True)):
            doc = etree.fromstring(res['arch'].encode('utf8'))
            elements = doc.xpath("/%s" % view_type)
            elements[0].set("create", "false")
            res['arch'] = etree.tostring(doc, pretty_print=True)
        return res
