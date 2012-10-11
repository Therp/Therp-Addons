# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2011 Therp BV (<http://therp.nl>).
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

import re
from osv import fields, osv
from tools.translate import _
import logging
from openerp import SUPERUSER_ID

logger = logging.getLogger('saved_selection')

class saved_selection(osv.osv):
    _description = 'Saved Selection'
    _name = 'saved_selection.selection'
    _rec_name = 'name'

    # Mind, should we override read method to only return ids of existing
    # resources? Currently not needed as it is only used in domain expressions.

    operations = {
        'add': lambda orig_ids, new_ids: list(set(orig_ids + new_ids)),
        'delete': lambda orig_ids, new_ids: [x for x in orig_ids if x not in new_ids],
        'intersect': lambda orig_ids, new_ids: [x for x in orig_ids if x in new_ids],
        }

    def compose_filter_domain(
        self, cr, uid, selection, model_pool, domain=None, context=None):
        """ Hook to allow for filter modules """
        return domain or []

    def update(
        self, cr, uid, model, mode, ids, domain, pass_ids = False, context=None):
        """ 
        Apply mutations on the user's saved selection
        and report back to the client

        :param model: The model should correspond to the model in the current
        user's saved selection
        :param mode: This is one of 'add', 'delete' or 'intersect'
        :param ids: a list of IDs to be processed
        :param domain: A search domain to be processed. The domain is only 
        processed if no ids are present. If both domain and ids are missing, 
        this will lead to all resources of the model being processed.
        TODO: can this lead to unintentional results?
        the 'ids' argument takes precedence.
        :param pass_ids: Wether or not to pass back the current content of
        the selection selection as a list of ids. To be used to refresh the
        domain of the current action if the call originates from the selection
        selection itself.
        :return: verbose summary of the mutation + list of ids, in case
        pass_ids == True
        :rtype: tuple(text, ids)

        Todo: translate summary messages
        """

        selection_id = False
        me = self.pool.get('res.users').read(
            cr, uid, uid, ['saved_selection_id'], context=context)
        if me['saved_selection_id']:
            selection_id = me['saved_selection_id'][0]
        else:
            # autoinitialize a new selection
            model_id = self.pool.get('ir.model').search(
                cr, uid,
                [('model', '=', model)], context=context)[0]
            selection_id = self.create(
                cr, uid, {'user_ids': [(6, 0, [uid])], 'model_id': model_id},
                context)

        # retrieve selection and check model
        selection = self.browse(cr, uid, selection_id, context)
        if selection.model_id.model != model:
            return (_("Error: selection is initialized for items of type %s") %
                    selection.model_id.name, False)

        model_obj = self.pool.get(model)

        search_context = context and context.copy() or {}
        # convert ids argument to domain
        if ids:
            domain = [('id', 'in', ids)]
            # There might be inactive ids, add active_test key
            # Note that active_test in the case of an added domain
            # should emphatically apply!
            search_context['active_test'] = False

        # apply communication filters
        filter_domain = self.compose_filter_domain(
            cr, uid, selection, model_obj, context=context)

        if filter_domain or not ids:
            ids = model_obj.search(
                cr, uid, domain + filter_domain, limit=0, context=search_context)

        # perform mutations
        orig_ids = selection.ids and [
                    int(x) for x in selection.ids.split(',')] or []
        new_ids = self.operations[mode](orig_ids, ids)
        self.write(
            cr, uid, selection_id, {
                'ids': ','.join([str(x) for x in new_ids])
                }, context=context
            )

        new_len = len(new_ids)
        mutations = new_len - len(orig_ids)
        msg = (
            mutations > 0 and (
                _("%d added, total %d") % (mutations, new_len)
                ) or
            mutations < 0 and (
                _("%d removed, total %d") % (abs(mutations), new_len)
                ) or
            (_("Nothing to do, total %d") % new_len)
            )
        return (msg, pass_ids and new_ids or [])

    def _check_ids(self, cr, uid, ids, context=None):
        # ensure that the saved list of numeric ids is indeed that
        for selection in self.read(cr, uid, ids, ['ids'], context):
            if selection['ids'] and not re.match("(\d+)(,\d+)*", selection['ids']):
                return False
        return True

    def selection_init(self, cr, uid, context=None):
        """
        When the user clicks the init icon in the web client,
        create the initialization wizard resource and return
        the action.
        """

        # Retrieve translated version of wizard's name. 
        # Can be done easier, surely.
        model_obj = self.pool.get('ir.model')
        model_ids = model_obj.search(
            cr, uid, [('model', '=', 'saved_selection.selection.init')],
            context=context)
        wizard_name  =model_obj.read(
            cr, uid, model_ids, ['name'], context=context)[0]['name']
        
        # Create wizard resource
        wizard_obj = self.pool.get('saved_selection.selection.init')
        wizard_id = wizard_obj.create(cr, uid, {}, context)
        
        # Compose and return action
        return {
            'name': wizard_name,
            'views': [[False, 'form']],
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'saved_selection.selection.init',
            'domain': [],
            'context': context,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': wizard_id,
            'nodestroy': True,
            'nodestroy': True,
            }

    def get(self, cr, uid, context=None):
        """
        Return a tuple (model, ids) of the user's
        active selection or False
        """
        res = False
        me = self.pool.get('res.users').read(
            cr, uid, uid, ['saved_selection_id'], context=context)
        if me['saved_selection_id']:
            selection_id = me['saved_selection_id'][0]
            selection = self.read(
                cr, uid, selection_id, ['model_id', 'ids'], context)
            model = self.pool.get('ir.model').read(
                cr, uid, selection['model_id'][0], ['model'], context
                )['model']

            domain = [('id', 'in', (
                        selection['ids'] and
                        [int(x) for x in selection['ids'].split(',')] or []))]

            search_context = context and context.copy() or {}
            search_context['active_test'] = False

            ids = self.pool.get(model).search(
                cr, uid, domain, limit=0, context=search_context)

            res = (model, ids)
        return res
        
    def action_get(self, cr, uid, context=None):
        """ 
        When the user clicks the selection's icon in the web client,
        compose a default action for the model in the user's selection
        selection, and apply the domain of the user's selection.
        Return the action that contains all of this.

        Note that this is a 'fixed' action, only valid for the web client!
        See web/controllers/main.py:fix_view_modes() which we mimic here
        """
        if context is None:
            context = {}
        res = False

        selection_id = False
        me = self.pool.get('res.users').read(
            cr, uid, uid, ['saved_selection_id'], context=context)
        if me['saved_selection_id']:
            selection_id = me['saved_selection_id'][0]
            selection = self.read(
                cr, uid, selection_id, ['model_id', 'ids', 'name'], context)
            model = self.pool.get('ir.model').read(
                cr, uid, selection['model_id'][0], ['model'], context
                )['model']
            context['active_id'] = False
            context['active_ids'] = False
            context['active_model'] = model
            res = {
                'domain': [('id', 'in',
                            selection['ids'] and
                            [int(x) for x in selection['ids'].split(',')] or []
                            )],
                'name': (_('Saved Selection') + 
                         (selection['name'] and (' %s' % selection['name']) or '') +
                         ' (' + selection['model_id'][1] + ')'),
                'res_model': model,
                'views': [(False, view_type) for view_type in 
                          ('list', 'page', 'form')],
                'type': 'ir.actions.act_window',
                'target': 'current',
                'limit': 80,
                'auto_search': True,
                'is_saved_selection': True,
                }
        return res

    def _get_active(self, cr, uid, ids, name, arg, context=None):
        res = dict([(x, False) for x in ids])
        selection_id = False
        me = self.pool.get('res.users').read(
            cr, uid, uid, ['saved_selection_id'], context=context)
        if me['saved_selection_id']:
            selection_id = me['saved_selection_id'][0]
            for res_id in ids:
                if res_id == selection_id:
                    res[res_id] = True
        return res

    def _set_active(self, cr, uid, res_id, field_name, field_value, arg, context=None):
        res = False
        if res_id:
            user_obj = self.pool.get('res.users')
            if field_value:
                res = user_obj.write(
                    cr, SUPERUSER_ID, uid, {'saved_selection_id': res_id})
            else:
                selection_id = False
                me = user_obj.read(
                    cr, uid, uid, ['saved_selection_id'], context=context)
                if me['saved_selection_id']:
                    selection_id = me['saved_selection_id'][0]
                    if selection_id == res_id:
                        res = user_obj.write(
                            cr, SUPERUSER_ID, uid, {'saved_selection_id': False})
        return res

    _columns = {
        'name': fields.char('Name', size=48),
        'user_ids': fields.many2many(
            'res.users', 'saved_selection_user_rel',
            'selection_id', 'user_id', 'User Access',
            required=True,
            ),
        'model_id': fields.many2one(
            'ir.model', 'Model',
            required=True, ondelete='cascade', readonly=True,
            help='Deze instelling kan achteraf niet meer gewijzigd worden.'
            ),
        'ids': fields.text('List of IDS', readonly=True),
        'no_call': fields.boolean(
            'Honour a no call flag', readonly=True,
            help='Deze instelling kan achteraf niet meer gewijzigd worden.'
            ),
        'no_email': fields.boolean('Honour a no e-mail flag', readonly=True,
            help='Deze instelling kan achteraf niet meer gewijzigd worden.'
            ),
        'no_snail': fields.boolean('Honour a no mail flag', readonly=True,
            help='Deze instelling kan achteraf niet meer gewijzigd worden.'
            ),
        'active_selection': fields.function(
            _get_active, type="boolean", string="Active Selection",
            fnct_inv = _set_active),
        'create_date': fields.datetime('Creation date', readonly=True),
        }        

    def get_default_model(self, cr, uid, context=None):
        model_obj = self.pool.get('ir.model')
        return model_obj.search(
            cr, uid, [('model', '=', 'res.partner')],
            context=context)[0]

    _defaults = {
        'user_ids': lambda self,cr,uid,context=None: [(6, 0, [uid])],
        'model_id': get_default_model,
        'active_selection': True,
        }

    _constraints = [
        (_check_ids, _('Error: not a valid list of resource ids.'), ['ids'])
        ]

#class saved_selection_wizard_my(osv.TransientModel):
#    """ 
#    This class to be used to display
#    the selection of resources in the GTK client
#    """
#    _name = 'saved_selection.selection.wizard.my'
