openerp.trp_web_x2x_matrix=function(openerp)
{
    openerp.web.form.widgets.add('one2many_matrix', 'openerp.trp_web_x2x_matrix.one2many_matrix');
    openerp.trp_web_x2x_matrix.one2many_matrix=openerp.web.form.FieldOne2Many.extend(
            {
                load_views: function()
                {
                    var deferred=this._super.apply(this, arguments);
                    this.viewmanager.registry=this.viewmanager.registry.extend({
                                    list: 'openerp.trp_web_x2x_matrix.One2ManyMatrixView',
                                });
                    _.each(this.views, function(view)
                        {
                            view.options.addable=false;
                            view.options.deletable=false;
                            view.options.isClarkGable=false;
                            view.options.sortable=false;
                            view.options.reordable=false;
                            view.options.pager=false;
                            view.options.action_buttons=false;
                        });
                    return deferred;
                }
            });
    openerp.trp_web_x2x_matrix.One2ManyMatrixView=openerp.web.form.One2ManyListView.extend(
            {
                init: function(parent, dataset, view_id, options)
                {
                    this._super(parent, dataset, view_id, options);
                    this.options=_.extend(this.options, {ListType: openerp.trp_web_x2x_matrix.One2ManyMatrixList}); 
                    this._limit=0;
                }
            });
    openerp.trp_web_x2x_matrix.One2ManyMatrixList=openerp.web.form.One2ManyList.extend(
            {
                init: function()
                {
                    return this._super.apply(this, arguments);
                },
                render: function ()
                {
                    if (this.view.o2m.readonly || this.view.o2m.view.widget_parent.active_view!='form')
                    {
                        this.options.editable=false;
                        return this._super.apply(this, arguments);
                    }
                    if (this.$current) 
                    {
                        this.$current.remove();
                    }
                    this.$current = this.$_element.clone(true);
                    var self=this;
                    jQuery.each(this.records.records, function(index, record)
                        {
                            var $new_row=jQuery('<tr>', {
                                                        id: _.uniqueId('oe-editable-row-'),
                                                        'data-record_id': record.attributes['id'],
                                                        'class': ' oe_forms',
                                                        click: function (e) {e.stopPropagation();}});
                            self.dataset.index=index;
                            var rowobj=_.extend(new openerp.web.ListEditableFormView(self.view, self.dataset, false), {
                                                    form_template: 'ListView.row.form',
                                                    registry: openerp.web.list.form.widgets,
                                                    $element: $new_row,
                                                    reload: function() {
                                                        //doing nothing
                                                    }
                                                })
                            jQuery.when(rowobj.on_loaded(self.get_form_fields_view())).then(function()
                                {
                                    rowobj.do_show();
                                    $new_row.find('td:last').remove();
                                    $new_row.appendTo(self.$current);
                                    $new_row.change(function()
                                        {
                                            self.edition=true;
                                            self.edition_id=rowobj.datarecord.id;
                                            self.dataset.index=index;
                                            self.edition_form=rowobj;
                                            self.save_row();

                                        });
                                });
                        });
                },
                cancel_pending_edition: function ()
                {
                    var cancelled=$.when();
                    if (this.edition_id)
                    {
                        cancelled = this.reload_record(this.records.get(this.edition_id));
                    }
                    return cancelled;
                }
            });

    openerp.web.form.FieldMany2One.include({
            on_ui_change: function()
            {
                this._super.apply(this, arguments);
                this.$input.change();
            }});
}
