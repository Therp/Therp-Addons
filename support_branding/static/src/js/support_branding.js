/* 

   Copyright (C) 2012-2015 Therp BV
   License: GNU AFFERO GENERAL PUBLIC LICENSE
            Version 3 or any later version

   Usage: if you run an OpenERP support company and you support
   customers without an OPW, you can brand the OpenERP instance
   accordingly using this module. Please enter the two variables
   in the code below, 'support_name' and 'support_link'. They will
   replace the unfriendly message about the OpenERP instance not
   being supported.
           
 */
   
openerp.support_branding = function(instance) {
    var QWeb = instance.web.qweb,
    _t = instance.web._t;
    
    instance.web.CrashManager.include({
        show_error: function(error)
        {
            this._super.apply(this, arguments);
            var ir_config_parameter = new openerp.web.Model('ir.config_parameter');
            var form = jQuery('.support-branding-submit-form');
            ir_config_parameter.call(
                'get_param', ['support_branding.support_email']).then(
                function(email)
                {
                    form.attr('action', 'mailto:' + email);
                });
            ir_config_parameter.call(
                'get_param', ['support_branding.company_name']).then(
                function(name)
                {
                    var button = form.find('button');
                    button.text(
                        _.str.sprintf(
                            openerp.web._t('Email to %s'), name));
                });
            form.prependTo(
                form.parents('.modal-dialog').find('.modal-footer'));
        }
    });
};
