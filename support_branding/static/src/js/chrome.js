/* 

   Copyright (C) 2012 Therp BV
   License: GNU AFFERO GENERAL PUBLIC LICENSE
            Version 3 or any later version

   Usage: if you run an OpenERP support company and you support
   customers without an OPW, you can brand the OpenERP instance
   accordingly using this module. Please enter the two variables
   in the code below, 'support_name' and 'support_link'. They will
   replace the unfriendly message about the OpenERP instance not
   being supported.
           
 */
   
openerp.support_branding = function(openerp) {

    /* Fill in the data of your supporting company */

    var support_name = 'Example Co Ltd.';
    var support_link = 'http://example.com';

    /* End of configurable settings */

    var QWeb = openerp.web.qweb,
    _t = openerp.web._t;
    
    openerp.web.CrashManager = openerp.web.CrashManager.extend({
        on_traceback: function(error) {
            if (openerp.connection.openerp_entreprise) {
                return this._super(error);
            }
            var dialog = new openerp.web.Dialog(this, {
                title: "OpenERP " + _.str.capitalize(error.type),
                width: '80%',
                height: '50%',
                min_width: '800px',
                min_height: '600px',
                buttons: [
                    {text: _t("Ok"), click: function() { $(this).dialog("close"); }}
                ]
            }).open();
            dialog.$element.html(QWeb.render('CrashManagerError', {
                session: openerp.connection,
                error: error,
                support_name: support_name,
                support_link: support_link,
            }));
        },
    });

    openerp.webclient.session.on_session_valid.add_last(function () {
        if (!openerp.webclient.session.openerp_entreprise) {
            openerp.webclient.$element.find('.oe_footer_powered').replaceWith(
                '<p class="oe_footer_powered">Powered by ' +
                    '<a href="http://www.openerp.com">OpenERP</a> - ' +
                    'Supported by <a href="' + support_link + 
                    '" target="_blank">' + support_name +
                    '</a></span><p>'
            );
            document.title = openerp.web._t(
                "OpenERP");
        }
    });
};


