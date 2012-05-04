/* 

   Copyright (C) 2012 Therp BV
   License: GNU AFFERO GENERAL PUBLIC LICENSE
            Version 3 or any later version

 */
   
openerp.base_report_creator = function(openerp) {

openerp.web_graph.GraphView = openerp.web_graph.GraphView.extend({
    start: function() {
        /* 
           Add context to the loading of the views and fields
           as it contains the custom report id

           This method overwrites the original GraphView.start()
           method. Can't have too many modules do that.
        */
        var self = this;

        /* How to call super's super?
           Replacing "this._super();"
        */
        openerp.web.View.prototype.start.apply(this, arguments)
        
        var loaded;
        var context = new openerp.web.CompoundContext(this.dataset.get_context());
        if (this.embedded_view) {
            loaded = $.when([self.embedded_view]);
        } else {
            loaded = this.rpc('/web/view/load', {
                    model: this.dataset.model,
                    view_id: this.view_id,
                    view_type: 'graph',
                    context: context
            });
        }
        return $.when(
            this.dataset.call_and_eval('fields_get', [false, context], null, 1),
            loaded)
            .then(function (fields_result, view_result) {
                self.fields = fields_result[0];
                self.fields_view = view_result[0];
                self.on_loaded(self.fields_view);
            });
    },
});
};


