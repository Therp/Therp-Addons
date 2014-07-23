/* 

   Copyright (C) 2012 Therp BV
   License: GNU AFFERO GENERAL PUBLIC LICENSE
            Version 3 or any later version

   Allow developers to define a warning in their act_window definition,
   similar to a warning in an on_change method's return value.

 */
   
openerp.trp_act_window_warning = function(openerp) {

    var QWeb = openerp.web.qweb,
    _t = openerp.web._t;

    openerp.web.ViewManagerAction = openerp.web.ViewManagerAction.extend({
        start: function() {
            var res = this._super();
            if (!_.isEmpty(this.action.warning)) {
                $(QWeb.render("CrashManagerWarning", this.action.warning)).dialog({
                    modal: true,
                    buttons: [
                        {text: _t("Ok"), click: function() { $(this).dialog("close"); }}
                ]
                });
            }
            return res;
        },
    });
};


