# -*- coding: utf-8 -*-
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
from tools.translate import _

class use_case(osv.osv):
    _name = 'use_case'
    _description = 'Use Case'
    _order = 'collection_id, sequence'
    _columns = {
        'sequence': fields.integer(
            'Sequence',
            ),
        'name': fields.char(
            'Name', size=128,
            required=True,
            ),
        'actor': fields.char(
            'Actor', size=128,
            required=True,
            ),
        'precondition': fields.text(
            'Precondition',
            ),
        'description': fields.text(
            'Description',
            required=True,
            ),
        'result': fields.text(
            'Result',
            required=True,
            ),
        'exceptions': fields.text(
            'Exceptions'),
        'implementation': fields.text(
            'Implementation'),
        'workload_ids': fields.one2many(
            'use_case.workload', 'use_case_id',
            'Workload'),
        'collection_id': fields.many2one(
            'use_case.collection', 'Use case set',
            required=True,
            ),
        }

    _defaults = {
        'sequence': 10,
        }

use_case()


class use_case_workload(osv.osv):
    _name = 'use_case.workload'
    _description = 'Use case workload'
    _order = 'use_case_id, sequence'
    _columns = {
        'name': fields.char(
            'Description', size=128,
            required=True,
            ),
        'hours': fields.float(
            'Hours'),
        'optional': fields.boolean(
            'Optional'),
        'use_case_id': fields.many2one(
            'use_case',
            required=True),
        'sequence': fields.integer(
            'Sequence',
            required=True,
            ),
        }

    _defaults = {
        'sequence': 10,
        }

use_case_workload()


class use_case_collection(osv.osv):
    _name = 'use_case.collection'
    _description = 'Set of use cases'

    def _get_hours_total(
        self, cr, uid, ids, field, args, context=None):
        result = {}
        for collection in self.browse(cr, uid, ids, context=context):
            result[collection.id] = {
                'hours_total': 0.0,
                'hours_total_optional': 0.0,
                }
            for use_case in collection.use_case_ids:
                for workload in use_case.workload_ids:
                    result[collection.id]['hours_total'] += workload.hours
                    if workload.optional:
                        result[collection.id]['hours_total_optional'] += workload.hours
            result[collection.id]['hours_total_nonoptional'] = (
                result[collection.id]['hours_total'] -
                result[collection.id]['hours_total_optional'])
        return result

    _columns = {
        'name': fields.char(
            'Name', size=128,
            required=True,
            ),
        'partner_id': fields.many2one(
            'res.partner', 'Partner'),
        'use_case_ids': fields.one2many(
            'use_case', 'collection_id',
            'Use cases',
            required=True,
            ),
        'create_date': fields.datetime(
            'Creation Date', readonly=True),
        'create_uid': fields.many2one(
            'res.users', 'Created by', readonly=True),
        'hours_total': fields.function(
            _get_hours_total, multi="hours",
            string="Total nr. of hours"),
        'hours_total_optional': fields.function(
            _get_hours_total, multi="hours",
            string="Total nr. of optional hours"),
        'hours_total_nonoptional': fields.function(
            _get_hours_total, multi="hours",
            string="Total nr. of non optional hours"),
        }

use_case_collection()
