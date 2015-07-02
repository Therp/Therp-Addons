openerp.trp_web_click2call = function(instance) {
    var QWeb = instance.web.qweb,
    _t = instance.web._t;

    var click2call = function(self){
            if (!self.get_value() || !self.is_valid()) {
                self.do_warn(_t("Error"), _t("Invalid phone number"));
            } else {
                var model = new instance.web.Model(
                    "click2call.click2call", self.build_context());
                model.call(
                    'callPBX', [[], self.get_value()],
                    {context: model.context()})
                .then(
                    function(action) {
                        self.do_notify(_t("Calling"), self.get_value());
                        self.do_action(action);
                    }
                );
            }
    }

    instance.web.form.Click2call = instance.web.form.FieldChar.extend({
        template: 'click2call',
        initialize_content: function() {
            this._super.apply(this, arguments);
            this.$el.find('button').click(this.on_button_clicked);
        },
        on_button_clicked: function() {
            click2call(this);
        }
    });

    instance.web.form.widgets.add('click2call', 'openerp.web.form.Click2call');

    instance.trp_web_click2call.click2call = click2call;
    instance.trp_web_click2call.click2call_number = function(number)
    {
        return this.click2call(
                {
                    get_value: function() { return number },
                    is_valid: function() { return true },
                    session: instance.session,
                    build_context: function() { return {} },
                    do_action: function() {},
                    do_notify: instance.webclient.do_notify,
                });
    };
}
