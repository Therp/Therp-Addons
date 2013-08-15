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
                    lambda x, y: -cmp(x[1], y[1]))])

class find_memory_leaks(TransientModel):
    _name = 'find.memory.leaks'

    _columns = {
            'output': fields.text('Output'),
            'graph': fields.binary('Graph'),
            'typestats_last': fields.text('typestats last'),
            }

    _defaults = {
        }

    def button_typestats(self, cr, uid, ids, context=None):
        current_stats = objgraph.typestats()
        for this in self.browse(cr, uid, ids, context=context):
            if this.typestats_last:
                stats = pickle.loads(this.typestats_last)
            else:
                stats = {}

            delta = dict(
                        filter(lambda x: x[1] != 0,
                            [(name, current_stats[name] - stats.get(name, 0))
                                for name in current_stats]))

            this.write(
                    {
                        'typestats_last': pickle.dumps(current_stats),
                        'output': sorted_dict_to_str(delta),
                    })

    def button_get_leaking_objects(self, cr, uid, ids, context=None):
        leaking_objects = objgraph.get_leaking_objects()
        for this in self.browse(cr, uid, ids, context=context):
            this.write(
                    {'output':
                        str(len(leaking_objects))+'\n'+
                        '\n'.join([str(type(o))
                            for o in leaking_objects])
                    })

    def button_count_leaking_objects(self, cr, uid, ids, context=None):
        leaking_objects = objgraph.get_leaking_objects()
        count = {}
        for o in leaking_objects:
            count[str(type(o))] = count.get(str(type(o)), 0) + 1
        for this in self.browse(cr, uid, ids, context=context):
            this.write(
                    {'output':
                        str(len(leaking_objects))+'\n'+
                        sorted_dict_to_str(count),
                    })

    def button_gc_collect(self, cr, uid, ids, context=None):
        gc.collect()
