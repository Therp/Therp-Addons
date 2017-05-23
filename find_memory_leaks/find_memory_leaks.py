# -*- coding: utf-8 -*-
# © 2013-2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
import objgraph
import pickle
import gc
from openerp.osv.orm import TransientModel
from openerp.osv import fields


def sorted_dict_to_str(d):
    return '\n'.join(
        [name + ': ' + str(count)
            for name, count in
                sorted(
                    d.iteritems(),
                    lambda x, y: -cmp(x[1], y[1])
                )])


class FindMemoryLeaks(TransientModel):
    _name = 'find.memory.leaks'

    _columns = {
        'output': fields.text('Output'),
        'graph': fields.binary('Graph'),
        'typestats_last': fields.text('typestats last'),
    }

    def redisplay(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'find.memory.leaks',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': ids[0],
            'views': [(False, 'form')],
            'target': 'new',
        }

    def button_typestats(self, cr, uid, ids, context=None):
        current_stats = objgraph.typestats()
        this = self.browse(cr, uid, ids, context=context)[0]
        if this.typestats_last:
            stats = pickle.loads(this.typestats_last)
        else:
            stats = {}
        delta = dict(
            filter(
                lambda x: x[1] != 0,
                [(name, current_stats[name] - stats.get(name, 0))
                    for name in current_stats]))
        this.write({
            'typestats_last': pickle.dumps(current_stats),
            'output': sorted_dict_to_str(delta),
        })
        return self.redisplay(cr, uid, ids, context=context)

    def button_get_leaking_objects(self, cr, uid, ids, context=None):
        leaking_objects = objgraph.get_leaking_objects()
        this = self.browse(cr, uid, ids, context=context)[0]
        this.write({
            'output':
            str(len(leaking_objects)) + '\n' +
            '\n'.join([
                str(type(o))
                for o in leaking_objects])
        })
        return self.redisplay(cr, uid, ids, context=context)

    def button_count_leaking_objects(self, cr, uid, ids, context=None):
        leaking_objects = objgraph.get_leaking_objects()
        count = {}
        for o in leaking_objects:
            count[str(type(o))] = count.get(str(type(o)), 0) + 1
        this = self.browse(cr, uid, ids, context=context)[0]
        this.write({
            'output':
                str(len(leaking_objects)) + '\n' +
                sorted_dict_to_str(count),
        })
        return self.redisplay(cr, uid, ids, context=context)

    def button_gc_collect(self, cr, uid, ids, context=None):
        gc.collect()
        return self.redisplay(cr, uid, ids, context=context)
