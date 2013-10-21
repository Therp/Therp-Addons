/* 

   Copyright (C) 2013 Therp BV
   License: GNU AFFERO GENERAL PUBLIC LICENSE
            Version 3 or any later version

*/

openerp.web_mode_visibility_separator = function (openerp) {
    openerp.web.form.Widget.include({

        /* Natively, this method exists on Fields widget
        that inherits from the form widget, not on the form
        widget itself that the separator widget inherits from
        */
        get_definition_options: function() {
            if (!this.definition_options) {
                var str = this.node.attrs.options || '{}';
                this.definition_options = JSON.parse(str);
            }
            return this.definition_options;
        },

        init: function(view, node) {
            this._super(view, node);
            if (! this.invisible) {
                var options = this.get_definition_options();
                if (this.view.form_template == "PageView") {
                    this.invisible = options.page_invisible;
                }
                else if (this.view.form_template == "FormView") {
                    this.invisible = options.form_invisible;
                }
            }
        },

    });
}
