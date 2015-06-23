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
        init: function()
        {
            var self = this,
                ir_config_parameter = new openerp.web.Model('ir.config_parameter');
            ir_config_parameter.call(
                'get_param', ['support_branding.support_email']).then(
                function(email)
                {
                    self.support_branding_support_email = email;
                });
            ir_config_parameter.call(
                'get_param', ['support_branding.company_name']).then(
                function(name)
                {
                    self.support_branding_company_name = name;
                });
            ir_config_parameter.call(
                'get_param', ['support_branding.support_text_prefix']).then(
                function(text_prefix)
                {
                    self.support_branding_support_text_prefix = text_prefix;
                });
            return this._super(this, arguments);
        },
        show_error: function(error)
        {
            var self = this;
            this._super.apply(this, arguments);
            jQuery('.support-branding-submit-form').each(function()
            {
                var $form = jQuery(this),
                    $button = $form.find('button'),
                    $body = $form.find("input[name='body']");
                if(self.support_branding_support_email)
                {
                    $form.attr(
                        'action',
                        'mailto:' + self.support_branding_support_email);
                }
                if(self.support_branding_company_name)
                {
                    $button.text(
                        _.str.sprintf(
                            openerp.web._t('Email to %s'),
                            self.support_branding_company_name));
                }
                if(self.support_branding_support_text_prefix)
                {
                    var stacktrace = $body.attr('value');
                    $body.attr(
                        'value', self.support_branding_support_text_prefix + stacktrace);
                }
                $form.prependTo(
                    $form.parents('.modal-dialog').find('.modal-footer'));
            });
        }
    });
};
