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
from difflib import unified_diff
from osv import fields, osv, orm
from datetime import datetime
from tools.translate import _

# Forward declarations for 6.0
class use_case_collection(osv.osv):
    _name = 'use_case.collection'
use_case_collection()

class use_case_workload(osv.osv):
    _name = 'use_case.workload'
use_case_workload()

class use_case_actor(osv.osv):
    _name = 'use_case.actor'
    _description = 'Actor'
    _columns = {
        'name': fields.char(
            'Name', size=64,
            required=True),
        'collection_id': fields.many2one(
            'use_case.collection',
            'Set of use cases',
            required=True),
        }
use_case_actor()


class use_case_version_tag(osv.osv):
    _name = 'use_case.version_tag'
    _description = 'Version tag'
    _columns = {
        'name': fields.char(
            'Name', size=64,
            required=True),
        'date': fields.date(
            'Date',
            required=True),
        'user': fields.char(
            'Editor', size=64,
            required=True),
        'collection_id': fields.many2one(
            'use_case.collection', 'Use case set',
            required=True,
            ),
        }

    _defaults = {
        'date': lambda self, cr, uid, c: datetime.now().strftime('%Y-%m-%d'),
        'user': lambda self, cr, uid, c: self.pool.get('res.users').read(cr, uid, uid, ['name'], context=c)['name'],
        }        
use_case_version_tag()


class use_case_history(orm.Model):
    _name = 'use_case.history'
    _description = 'Use Case History'
    _order = 'use_case_id, create_date desc'
    _rec_name = 'create_date'

    _columns = {
        'use_case_id': fields.many2one(
            'use_case', 'Use Case', readonly=True,
            required=True, ondelete='CASCADE'),
        'description': fields.text(
            'Descripion', readonly=True, select=1),
        'diff': fields.text(
            'Diff', readonly=True, select=1),
        'create_date': fields.datetime(
            'Changed at', readonly=True),
        'create_uid': fields.many2one(
            'res.users', 'Changed by',
            required=True, ondelete='SET NULL',
            readonly=True),
        }


class use_case(osv.osv):
    _name = 'use_case'
    _description = 'Use Case'
    _order = 'collection_id, sequence'

    def historize(self, cr, uid, ids, vals, context=None, force=False):
        """
        If the description has changed, create a history item.

        The history item contains a full text representation of
        the modified parts, and a shorthand diff for easy comparison
        with the previous version.
        """
        if not ids:
            return True
        if isinstance(ids, (int, long)):
            ids = [ids]

        fields = [field for field in [
                'precondition',
                'description',
                'result',
                'exceptions',
                'implementation'] if field in vals.keys()]

        for use_case in self.read(
                cr, uid, ids, fields, context=context):
            description = ''
            diff = ''
            for field in fields:
                value = (vals[field] or '').strip()
                if force or value != (use_case[field] or '').strip():
                    description += '- %s changed to:\n%s\n\n' % (field, value)
                if value != (use_case[field] or '').strip():
                    for line in unified_diff(
                            (use_case[field] or '').strip().split('\n'),
                            value.split('\n'), fromfile=field, tofile=field):
                        diff += "%s\n" % line.strip()
                    diff += '\n'
            if description:
                self.pool.get('use_case.history').create(
                    cr, uid, {
                        'use_case_id': use_case['id'],
                        'description': description,
                        'diff': diff,
                        }, context=context)
        return True

    def write(self, cr, uid, ids, vals, context=None):
        """
        Call to historize()
        """
        self.historize(cr, uid, ids, vals, context=context)
        return super(use_case, self).write(
            cr, uid, ids, vals, context=context)

    def create(self, cr, uid, vals, context=None):
        """
        Call to historize(). Use force=True, because the description will
        be the same as on the created use case.
        """
        result = super(use_case, self).create(
            cr, uid, vals, context=context)
        self.historize(cr, uid, result, vals, context=context, force=True)
        return result

    def _get_use_case_hours(
        self, cr, uid, ids, field, args, context=None):
        result = {}
        for use_case in self.browse(cr, uid, ids, context=context):
            result[use_case.id] = {
                'hours': 0.0,
                'hours_optional': 0.0,
                }
            for workload in use_case.workload_ids:
                result[use_case.id]['hours'] += workload.hours
                if workload.optional:
                    result[use_case.id]['hours_optional'] += workload.hours
            result[use_case.id]['hours_nonoptional'] = (
                result[use_case.id]['hours'] -
                result[use_case.id]['hours_optional'])
        return result

    def _get_number(self, cr, uid, ids, *args, **kwargs):
        """
        Retrieve the sequential number of the use case
        within the use case set
        """
        res = dict([(x, 0) for x in ids])
        cr.execute("""
            SELECT
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
        """, (tuple(ids),))
        res.update(dict(cr.fetchall()))
        return res

    _columns = {
        'active': fields.boolean(
            'Active'),
        'sequence': fields.integer(
            'Sequence',
            ),
        'number': fields.function(
            _get_number, type='integer',
            string='Number',
            ),
        'name': fields.char(
            'Name', size=128,
            required=True,
            ),
        'actor_ids': fields.many2many(
            'use_case.actor', 'use_case_actor_use_case_rel',
            'use_case_id', 'actor_id', 'Actors',
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
        'hours': fields.function(
            _get_use_case_hours, multi="hours", method=True,
            string="Nr. of hours"),
        'hours_optional': fields.function(
            _get_use_case_hours, multi="hours", method=True,
            string="Nr. of optional hours"),
        'hours_nonoptional': fields.function(
            _get_use_case_hours, multi="hours", method=True,
            string="Nr. of non-optional hours"),
        'task_id': fields.many2one(
            'project.task',
            'Task'),
        'state': fields.related(
            'task_id',
            'state',
            type='selection'),
        }

    _defaults = {
        'active': True,
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
                if use_case.active:
                    result[collection.id]['hours_total'] += use_case.hours
                    result[collection.id]['hours_total_optional'] += use_case.hours_optional
            result[collection.id]['hours_total_nonoptional'] = (
                result[collection.id]['hours_total'] -
                result[collection.id]['hours_total_optional'])
        return result

    def _get_id(self, cr, uid, ids, field, args, context=None):
        """ 
        Workaround for showing id field in 6.0 web client and prevent
        an unpickle error from showing up because 'id' is a reserved
        term in Python.
        By using the raw id in the domain and context, we can
        push the collection id to the use case form before it
        is saved first time.
        Eventually, this is only needed to be able to select a
        previously created actor in the use case form before
        the use case is saved. Sigh.
        """
        return dict([(x, x) for x in ids])

    _columns = {
        'res_id': fields.function(
            _get_id, type="integer", method=True,
            string='ID'),
        'name': fields.char(
            'Name', size=128,
            required=True,
            ),
        'description': fields.text(
            'Description'),
        'partner_id': fields.many2one(
            'res.partner', 'Partner'),
        'use_case_ids': fields.one2many(
            'use_case', 'collection_id',
            'Use cases',
            required=True,
            context={'active_test': False},
            ),
        'actor_ids': fields.one2many(
            'use_case.actor', 'collection_id',
            'Actors'),
        'version_tag_ids': fields.one2many(
            'use_case.version_tag', 'collection_id',
            'Version tags'),
        'create_date': fields.datetime(
            'Creation Date', readonly=True),
        'create_uid': fields.many2one(
            'res.users', 'Created by', readonly=True),
        'hours_total': fields.function(
            _get_hours_total, multi="hours", method=True,
            string="Total nr. of hours"),
        'hours_total_optional': fields.function(
            _get_hours_total, multi="hours", method=True,
            string="Total nr. of optional hours"),
        'hours_total_nonoptional': fields.function(
            _get_hours_total, multi="hours", method=True,
            string="Total nr. of non optional hours"),
        'project_id': fields.many2one(
            'project.project',
            'Project', help='The project related to this set of use cases'),
        'state': fields.related(
            'project_id',
            'state',
            type='selection'),
        }

    def action_create_tasks(self, cr, uid, ids, context=None):
        for this in self.browse(cr, uid, ids, context):
            if not this.project_id:
                this.write({
                    'project_id': self.pool.get('project.project').create(cr,
                        uid, {
                            'name': this.name, 
                            'partner_id': this.partner_id.id
                            },
                        context),
                    })
                this.refresh()
            for use_case in this.use_case_ids:
                if not use_case.task_id:
                    use_case.write(
                            {
                                'task_id': 
                                    self.pool.get('project.task').create(
                                        cr, uid,
                                        {
                                            'name': use_case.name,
                                            'project_id': this.project_id.id,
                                            'partner_id': this.partner_id.id,
                                            'planned_hours': use_case.hours,
                                            'remaining_hours': use_case.hours,
                                            'use_case_id': use_case.id,
                                        }, context)
                            })

use_case_collection()


