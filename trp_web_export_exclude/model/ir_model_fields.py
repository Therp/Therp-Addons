from osv import fields, osv, orm
from openerp.addons.web.controllers.main import Export
from openerp.addons.web.common import http


class ir_model_fields(osv.osv):
    _inherit = 'ir.model.fields'
    _columns = {
        'export_exclude': fields.boolean('Exclude from export'),
        }

    def write(self, cr, user, ids, vals, context=None):
        """
        The super method does not allow a write on any non-manual field.
        Therefore, circumvent the ORM when writing a value for
        'export_exclude'.
        """
        if vals and 'export_exclude' in vals:
            if ids:
                if isinstance(ids, (int, long)):
                    ids2 = [ids]
                else:
                    ids2 = ids
                cr.execute(
                    "UPDATE ir_model_fields"
                    " SET export_exclude = " +
                    (vals['export_exclude'] and 'true' or 'false') +
                    " WHERE id in %s", (tuple(ids2),)
                    )
            vals.pop('export_exclude')
        if vals:
            return super(ir_model_fields, self).write(
                cr, user, ids, vals, context=context)
        return True

def fields_get_exclude(
    self, cr, user, context=None):
    fields_pool = self.pool.get('ir.model.fields')
    if 'export_exclude' in fields_pool._columns:
        field_ids = fields_pool.search(
            cr, 1, [('model', '=', self._name), ('export_exclude', '=', True)])
        fields = fields_pool.read(cr, 1, field_ids, ['name'])
        return [x['name'] for x in fields]
    return []

orm.BaseModel.fields_get_exclude = fields_get_exclude

def fields_get(
        self, cr, uid, allfields=None, context=None, write_access=True):
    """
    Assign export_exclude to the results of fields_get
    """
    res = self.fields_get_orig(
        cr, uid, allfields=allfields, context=context,
        write_access=write_access)

    if 'export_exclude' not in self.pool.get('ir.model.fields')._columns:
        return res
    cr.execute("""SELECT name FROM ir_model_fields
                  WHERE model = %s AND export_exclude is true""", (self._name,))
    excluded_fields = [x[0] for x in cr.fetchall()]
    for field in excluded_fields:
        if field in res:
            res[field]['export_exclude'] = True
    return res
        
orm.BaseModel.fields_get_orig = orm.BaseModel.fields_get
orm.BaseModel.fields_get = fields_get

Export.get_fields_orig = Export.get_fields

@http.jsonrequest
def get_fields(
    self, req, model, prefix='', parent_name= '',
    import_compat=True, parent_field_type=None,
    exclude=None):
    if not exclude:
        Model = req.session.model(model)
        exclude = Model.fields_get_exclude()
    # Below is a nearly verbatim copy of the method from openerp-web/addons/web/controllers/main.py
    # Could not call it as super, as it is a decorated method
    if True: # masq the indentation difference with the copied method for easy upgrading
        if import_compat and parent_field_type == "many2one":
            fields = {}
        else:
            fields = self.fields_get(req, model)

        if import_compat:
            fields.pop('id', None)
        else:
            fields['.id'] = fields.pop('id', {'string': 'ID'})

        fields_sequence = sorted(fields.iteritems(),
            key=lambda field: field[1].get('string', ''))

        records = []
        for field_name, field in fields_sequence:
            # Therp: move this out of the import_compat condition
            if exclude and field_name in exclude:
                continue
            if import_compat:
                if field.get('readonly'):
                    # If none of the field's states unsets readonly, skip the field
                    if all(dict(attrs).get('readonly', True)
                           for attrs in field.get('states', {}).values()):
                        continue

            id = prefix + (prefix and '/'or '') + field_name
            name = parent_name + (parent_name and '/' or '') + field['string']
            record = {'id': id, 'string': name,
                      'value': id, 'children': False,
                      'field_type': field.get('type'),
                      'required': field.get('required'),
                      'relation_field': field.get('relation_field')}
            records.append(record)

            if len(name.split('/')) < 3 and 'relation' in field:
                ref = field.pop('relation')
                if import_compat:
                    record['value'] += '/id'
                record['params'] = {'model': ref, 'prefix': id, 'name': name}

                if not import_compat or field['type'] == 'one2many':
                    # m2m field in import_compat is childless
                    record['children'] = True

        return records

Export.get_fields = get_fields
