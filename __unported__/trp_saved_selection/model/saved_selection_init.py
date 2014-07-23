# -*- encoding: utf-8 -*-
from osv import osv, fields
from tools.translate import _
from openerp import SUPERUSER_ID

class saved_selection_init(osv.osv_memory):
    """
    TODO: on_change method on model to actually
    check for these no_ flags...
    """
    _name = 'saved_selection.selection.init'
    _description = 'Initialize Saved Selection'
    _columns = {
        'name': fields.char('Name', size=48),
        'model_id': fields.many2one('ir.model', 'Model', required=True),
        'discard_existing': fields.boolean('Discard current selection'),
        'existing': fields.boolean('Existing selection', readonly=True),
        }

    def get_default_model(self, cr, uid, context=None):
        """
        Default to the user's current model, or
        res.partner if there is none.
        """
        res = self.get_current_value(
            cr, uid, 'model_id', context=context)
        if res:
            res = res[0]
        else:
            model_obj = self.pool.get('ir.model')
            res = model_obj.search(
                cr, uid, [('model', '=', 'res.partner')],
                context=context)[0]
        return res

    def get_default_name(self, cr, uid, context=None):
        return self.get_current_value(
            cr, uid, 'name', context=context)

    def get_current_value(self, cr, uid, field, context=None):
        """
        Default to the user's current setting
        """
        res = False
        user_obj = self.pool.get('res.users')
        selection_obj = self.pool.get('saved_selection.selection')
        selection_id = user_obj.read(
            cr, uid, uid, ['saved_selection_id'],
            context=context)['saved_selection_id']
        if selection_id:
            res = selection_obj.read(
                cr, uid, selection_id[0], [field], context=context)[field]
        return res

    def get_existing(self, cr, uid, field, context=None):
        """
        Determine if there is an existing selection worth mentioning
        at init time. If not, the 'discard exsting' checkbox will not be shown
        """
        res = False
        user_obj = self.pool.get('res.users')
        selection_obj = self.pool.get('saved_selection.selection')
        selection_id = user_obj.read(
            cr, uid, uid, ['saved_selection_id'],
            context=context)['saved_selection_id']
        if selection_id:
            selection = selection_obj.read(
                cr, uid, selection_id[0], context=context)
            if (selection['name'] or selection['ids']
                or selection['user_ids'] and len(selection['user_ids']) > 1):
                return True
        return res
            
    _defaults = {
        'model_id': get_default_model,
        'name': get_default_name,
        'existing': get_existing,
        'discard_existing': True,
        }

    def compose_create_values(self, cr, uid, ids, values=None, context=None):
        """ Hook to allow for filters """
        if values is None:
            values = {}
        selection_init = self.browse(
            cr, uid, ids[0], context)
        values.update({
            'user_ids': [(6, 0, [uid])],
            'name': selection_init.name,
            'ids': False,
            })
        return values

    def selection_init(self, cr, uid, ids, context):
        '''
        '''
        selection_obj = self.pool.get('saved_selection.selection')
        user_obj = self.pool.get('res.users')
        values = self.compose_create_values(
            cr, uid, ids, values={}, context=context)
        discard = self.read(
            cr, uid, ids[0], ['discard_existing'],
            context=context)['discard_existing']
        selection_id = False
        me = user_obj.read(
            cr, uid, uid, ['saved_selection_id'], context=context)
        if me['saved_selection_id'] and discard:
            selection_obj.write(
                cr, uid, me['saved_selection_id'][0],
                values, context=context)
        else:
            selection_id = selection_obj.create(
                cr, uid, values, context=context)
            self.pool.get('res.users').write(
                cr, SUPERUSER_ID, uid, {'saved_selection_id': selection_id},
                context=context)
        return {'type': 'ir.actions.act_window_close'}
