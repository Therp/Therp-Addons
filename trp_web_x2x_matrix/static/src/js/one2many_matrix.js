openerp.trp_web_x2x_matrix=function(openerp)
{
    openerp.web.form.widgets.add('one2many_matrix', 'openerp.trp_web_x2x_matrix.one2many_matrix');
    openerp.trp_web_x2x_matrix.one2many_matrix=openerp.web.form.FieldOne2Many.extend(
            {
                load_views: function()
                {
                    this._super.apply(this, arguments);
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
                },
                get_value: function()
                {
                    jQuery.each(this.viewmanager.views[this.viewmanager.active_view].controller.widget_children, function(index, rowobj)
                            {
                                rowobj.do_save();
                            });
                    return this._super.apply(this, arguments);
                }
            });
    openerp.trp_web_x2x_matrix.One2ManyMatrixView=openerp.web.form.One2ManyListView.extend(
            {
                init: function(parent, dataset, view_id, options)
                {
                    this._super(parent, dataset, view_id, options);
                    this.options=_.extend(this.options, {ListType: openerp.trp_web_x2x_matrix.One2ManyMatrixList}); 
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
                    var find_active_view=function(widget)
                    {
                        if(typeof(widget.active_view)=='undefined' || widget.active_view=='list')
                        {
                            return find_active_view(widget.widget_parent);
                        }
                        return widget.active_view;                  
                    }
                    //TODO: there must be a better way to find out if we're in edit mode or not
                    if(find_active_view(this.view)!='form')
                    {
                        return this._super.apply(this, arguments);
                    }
                    var self = this;
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
                                                        'data-id': record['id'],
                                                        'class': ' oe_forms',
                                                        click: function (e) {e.stopPropagation();}});
                            self.dataset.index=index;
                            var rowobj=_.extend(new openerp.web.ListEditableFormView(self.view, self.dataset, false), {
                                                    form_template: 'ListView.row.form',
                                                    registry: openerp.web.list.form.widgets,
                                                    $element: $new_row
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
}
