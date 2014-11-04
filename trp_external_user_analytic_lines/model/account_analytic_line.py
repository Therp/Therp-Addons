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
from openerp.osv.orm import Model
from openerp.osv import fields


class AccountAnalyticLine(Model):
    _inherit = 'account.analytic.line'

    def _origin_get(self, cr, uid, ids, field_name, arg, context=None):
        result = dict([(i, False) for i in ids])
        cr.execute(
            '''
            select * from (
                select 'project.task', pt.id, aal.id, 1
                    from
                        project_task pt
                    join project_task_work ptw
                        on ptw.task_id=pt.id
                    join hr_analytic_timesheet hat
                        on ptw.hr_analytic_timesheet_id=hat.id
                    join account_analytic_line aal
                        on hat.line_id=aal.id
                    where aal.id in %(ids)s
                union
                select 'project.issue', pi.id, aal.id, 2
                    from
                        project_issue pi
                    join project_task_work ptw
                        on pi.task_id=ptw.task_id
                    join hr_analytic_timesheet hat
                        on ptw.hr_analytic_timesheet_id=hat.id
                    join account_analytic_line aal
                        on hat.line_id=aal.id
                    where aal.id in %(ids)s
            ) as possible_origins
            order by 4
            ''',
            {'ids': tuple(ids)})
        for row in cr.fetchall():
            result[row[2]] = '%s,%s' % (row[0], row[1])
        return result

    _columns = {
        'origin': fields.function(
            lambda self, cr, uid, ids, field_name, arg, context:
                self._origin_get(cr, uid, ids, field_name, arg,
                                 context=context),
            type='reference', string='Origin'),
    }

    def button_open_origin(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context=context):
            return {
                'type': 'ir.actions.act_window',
                'res_model': this.origin._table._name,
                'res_id': this.origin.id,
                'target': 'new',
                'view_type': 'form',
                'view_mode': 'page',
            }
