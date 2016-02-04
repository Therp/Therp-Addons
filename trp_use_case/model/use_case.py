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
from openerp import api, models, fields
from datetime import datetime


class use_case_actor(models.Model):
    _name = 'use_case.actor'
    _description = 'Actor'

    name = fields.Char('Name', required=True)
    collection_id = fields.Many2one(
        'use_case.collection', string='Set of use cases', required=True)


class use_case_version_tag(models.Model):
    _name = 'use_case.version_tag'
    _description = 'Version tag'

    name = fields.Char('Name', required=True)
    date = fields.Date(
        'Date', required=True,
        default=lambda self: datetime.now().strftime('%Y-%m-%d'))
    user = fields.Char(
        'Editor', required=True,
        default=lambda self:
        self.env['res.users'].browse([self.env.uid]).name)
    collection_id = fields.Many2one(
        'use_case.collection', string='Use case set', required=True)


class use_case(models.Model):
    _name = 'use_case'
    _description = 'Use Case'
    _order = 'collection_id, sequence'
    _inherit = 'mail.thread'

    @api.depends('workload_ids.hours', 'workload_ids.optional')
    def _get_use_case_hours(self):
        for use_case in self:
            values = {
                'hours': 0.0,
                'hours_optional': 0.0,
                }
            for workload in use_case.workload_ids:
                values['hours'] += workload.hours
                if workload.optional:
                    values['hours_optional'] += workload.hours
            values['hours_nonoptional'] = (
                values['hours'] - values['hours_optional'])
            # TODO: why doesn't this work?
            # use_case.write(values)
            use_case.hours = values['hours']
            use_case.hours_optional = values['hours_optional']
            use_case.hours_nonoptional = values['hours_nonoptional']

    @api.depends(
        'collection_id.use_case_ids', 'collection_id.use_case_ids.sequence',
        'collection_id.use_case_ids.active')
    def _get_number(self):
        """
        Retrieve the sequential number of the use case
        within the use case set
        """
        self.env.cr.execute(
            """SELECT
                id,
                (
                    SELECT COUNT(*)
                    FROM use_case
                    WHERE
                        collection_id = uc.collection_id
                        AND active = true
                        AND sequence <= uc.sequence
                )
            FROM use_case AS uc
            WHERE
            id in %s
            AND active = true
            ORDER BY collection_id, sequence
            """, (tuple(self.ids),))
        id2number = dict(self.env.cr.fetchall())
        for use_case in self:
            use_case.number = id2number.get(use_case.id)

    active = fields.Boolean('Active', default=True)
    sequence = fields.Integer('Sequence', default=10)
    number = fields.Integer(compute=_get_number, string='Number')
    name = fields.Char('Name', required=True)
    actor_ids = fields.Many2many(
        'use_case.actor',
        relation='use_case_actor_use_case_rel',
        column1='use_case_id',
        column2='actor_id',
        string='Actors')
    precondition = fields.Text('Precondition')
    description = fields.Text('Description', required=True)
    result = fields.Text('Result', required=True)
    exceptions = fields.Text('Exceptions')
    implementation = fields.Text('Implementation')
    workload_ids = fields.One2many(
        'use_case.workload', 'use_case_id', string='Workload')
    collection_id = fields.Many2one(
        'use_case.collection', string='Use case set', required=True)
    hours = fields.Float(
        compute=_get_use_case_hours, string="Nr. of hours")
    hours_optional = fields.Float(
        compute=_get_use_case_hours, string="Nr. of optional hours")
    hours_nonoptional = fields.Float(
        compute=_get_use_case_hours, string="Nr. of non-optional hours")


class use_case_workload(models.Model):
    _name = 'use_case.workload'
    _description = 'Use case workload'
    _order = 'use_case_id, sequence'

    name = fields.Char('Description')
    hours = fields.Float('Hours')
    optional = fields.Boolean('Optional')
    use_case_id = fields.Many2one('use_case', required=True)
    sequence = fields.Integer('Sequence', required=True, default=10)


class use_case_collection(models.Model):
    _name = 'use_case.collection'
    _description = 'Set of use cases'
    _inherit = 'mail.thread'

    state = fields.Selection([
                 ('draft', 'Draft'),
                 ('open', 'Open'),
                 ('done', 'Done'),
                 ], string="Status", help="Collection Status", default="draft", required = True)

    @api.multi
    def draft_statusbar(self):
        self.write({
            'state': 'draft'
        })

    @api.one
    def open_statusbar(self):
        self.write({
            'state': 'open'
        })

    @api.one
    def done_statusbar(self):
        self.write({
            'state': 'done'
        })

    @api.depends(
        'use_case_ids.active', 'use_case_ids.workload_ids.hours',
        'use_case_ids.workload_ids.optional')
    def _get_hours_total(self):
        for collection in self:
            values = {
                'hours_total': 0.0,
                'hours_total_optional': 0.0,
                'tot_use_cases': 0
                }
            for use_case in collection.use_case_ids:
                if use_case.active:
                    values['hours_total'] += use_case.hours
                    values['hours_total_optional'] += use_case.hours_optional
                    values['tot_use_cases'] += 1
            values['hours_total_nonoptional'] = (
                values['hours_total'] - values['hours_total_optional'])
            # TODO: why doesn't this work?
            # collection.write(values)
            collection.hours_total = values['hours_total']
            collection.hours_total_optional = values['hours_total_optional']
            collection.hours_total_nonoptional = \
                values['hours_total_nonoptional']
            collection.tot_use_cases = values['tot_use_cases']

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
    partner_id = fields.Many2one('res.partner', 'Partner')
    use_case_ids = fields.One2many(
        'use_case', 'collection_id', string='Use cases', required=True,
        context={'active_test': False})
    actor_ids = fields.One2many(
        'use_case.actor', 'collection_id', string='Actors')
    version_tag_ids = fields.One2many(
        'use_case.version_tag', 'collection_id', string='Version tags')
    hours_total = fields.Float(
        compute=_get_hours_total, string="Total nr. of hours")
    hours_total_optional = fields.Float(
        compute=_get_hours_total, string="Total nr. of optional hours")
    hours_total_nonoptional = fields.Float(
        compute=_get_hours_total, string="Total nr. of non optional hours")
    tot_use_cases = fields.Integer(
        compute=_get_hours_total, string="tot_use_cases")

