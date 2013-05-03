/* -----------------------------------------------------------\ 
 * web functions for trp_web_hide_buttons
 * --------------------------------------------------------- */

/* comments to control jslint */
/*jslint nomen: true, white: true, */
/*global window, openerp, $, _ */

openerp.trp_web_hide_buttons = function (openerp) {
    'use strict';

    /** Change ListView to not show Create and Delete buttons when that
    has been requested through the context passed from the action.
    */
    openerp.web.ListView.include({

        on_loaded : function () {
            var result, context;
            context = _.extend({}, this.dataset.get_context());
            if (context) {
                _.extend.apply(this, _.union([context], context.__contexts));

                if (context.nodelete) {
                    this.options.deletable=false;
                }
                if (context.noedit) {
                    this.options.isClarkGable=false;
                }
            }
            result = this._super.apply(this, arguments);
            if (context && context.nocreate) {
                this.$element.find('.oe-list-add')
                    .attr('disabled', true).hide();
            }
            return result;
        }
    });

    openerp.web.FormView.include({

        on_loaded : function (record) {
            var result, context;
            result = this._super.apply(this, arguments);
            context = _.extend({}, this.dataset.get_context());
            if (context) {
                _.extend.apply(this, _.union([context], context.__contexts));

                if (context.nocreate) {
                    this.$element.find('.oe_form_button_create')
                        .attr('disabled', true).hide();
                    this.$element.find('.oe_form_button_duplicate')
                        .attr('disabled', true).hide();
                }
                if (context.nodelete) {
                    this.$element.find('.oe_form_button_delete')
                        .attr('disabled', true).hide();
                }
            }
            return result;
        }
    });

    openerp.web_kanban.KanbanView.include({

        on_loaded : function (record) {
            var result, context;
            result = this._super.apply(this, arguments);
            context = _.extend({}, this.dataset.get_context());
            if (context) {
                _.extend.apply(this, _.union([context], context.__contexts));

                if (context.nocreate) {
                    this.$element.find('button.oe_kanban_button_new')
                        .attr('disabled', true).hide();
                }
            }
            return result;
        }
    });

};
