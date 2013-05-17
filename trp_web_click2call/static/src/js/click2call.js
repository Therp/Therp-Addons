openerp.trp_web_click2call = function(openerp) {
    var QWeb = openerp.web.qweb,
    _t = openerp.web._t;

    var click2call = function(self){
            if (!self.value || !self.is_valid()) {
                self.do_warn(_t("Error"), _t("Invalid phone number"));
            } else {
                var dataset = new openerp.web.DataSet(self, "click2call.click2call",
                                                      self.session.user_context);
                dataset.call(
                    'callPBX', 
                    [self.value, self.build_context()],
                    function(action) {
                        var widget = self;
                        while (widget.widget_parent && ! (widget.action_manager)) {
                            widget = widget.widget_parent;
                        }
                        if (widget.action_manager) {
                            widget.action_manager.do_action(action);
                        }
                        else {
                            alert("Cannot determine action manager");
                        }
                    }
                );
            }
    }

    openerp.web.form.Click2call = openerp.web.form.FieldChar.extend({
        template: 'click2call',
        start: function() {
            this._super.apply(this, arguments);
            var $button = this.$element.find('button');
            $button.click(this.on_button_clicked);
            this.setupFocus($button);
        },
        on_button_clicked: function() {
            click2call(this);
        }
    });

    openerp.web.page.Click2callReadonly = openerp.web.page.FieldCharReadonly.extend({
        template: 'click2call.readonly',
        start: function() {
            this._super.apply(this, arguments);
            var $button = this.$element.find('button');
            $button.click(this.on_button_clicked);
            this.setupFocus($button);
        },
        on_button_clicked: function() {
            click2call(this);
        }
    });

    openerp.web.form.widgets.add('click2call', 'openerp.web.form.Click2call');
    openerp.web.page.readonly.add('click2call', 'openerp.web.page.Click2callReadonly');

    openerp.trp_web_click2call.click2call = click2call;
    openerp.trp_web_click2call.click2call_number = function(number)
    {
        return this.click2call(
                {
                    value: number,
                    is_valid: function() { return true },
                    session: {user_context: openerp.connection.user_context},
                    build_context: function() { return {} },
                    action_manager: {do_action: function() {}},
                });
    };
}
