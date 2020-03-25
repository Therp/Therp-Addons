//-*- coding: utf-8 -*-
//Copyright 2020 Therp BV <https://therp.nl>
//License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

odoo.define('base_decision_tree', function(require) {
    var core = require('web.core'),
        web_editor_backend = require('web_editor.backend');
    // A html field that evaluates data-odoo-action-model,
    // data-odoo-action-id, data-odoo-action-views (json representation of
    // views list for action), data-odoo-action-target
    // (not yet) data-odoo-action attributes, default is to open the form
    // this might be useful for the community when it's a bit matured
    var FieldHtmlAction = web_editor_backend.FieldTextHtmlSimple.extend({
        render_value: function () {
            var result = this._super.apply(this, arguments);
            this.$('[data-odoo-action-model]').click(
                this.proxy('_html_action_click'));
            return result;
        },
        _html_action_click: function (e) {
            var self = this,
                $target = jQuery(e.currentTarget);
            return this.do_action({
                type: 'ir.actions.act_window',
                res_model: $target.data('odoo-action-model'),
                res_id: $target.data('odoo-action-id'),
                target: $target.data('odoo-action-target') || 'current',
                views:
                    $target.data('odoo-action-views')
                        ? JSON.parse($target.data('odoo-action-views'))
                        : [[false, 'form']],
                flags: {
                    initial_mode: $target.data('odoo-action-initial-mode') ||
                    'view',
                },
            }, {
                on_close: function () {
                    var current = self.getParent();
                    while (current.getParent() && !current.reload) {
                        current = current.getParent();
                    }
                    if (current) {
                        return current.reload();
                    }
                },
            });
        },
    });
    core.form_widget_registry.add('html_action', FieldHtmlAction);
    return {
        FieldHtmlAction: FieldHtmlAction,
    };
});
