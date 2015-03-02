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
                ir_config_parameter = new instance.web.Model('ir.config_parameter');
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
            return this._super(this, arguments);
        },
        show_error: function(error)
        {
            var self = this;
            this._super.apply(this, arguments);
            jQuery('.support-branding-submit-form').each(function()
            {
                var $form = jQuery(this),
                    $button = $form.find('button');
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
                            instance.web._t('Email to %s'),
                            self.support_branding_company_name));
                }
                $form.prependTo(
                    $form.parents('.ui-dialog').find('.ui-dialog-buttonpane'));
            });
        }
    });

    instance.web.WebClient.include({
        start: function()
        {
            var self = this,
                ir_config_parameter = new instance.web.Model('ir.config_parameter'),
                d1 = jQuery.Deferred(),
                d2 = jQuery.Deferred(),
                d3 = jQuery.Deferred();
            jQuery.when(this._super(this, arguments))
            .then(function()
            {
                if(!self.session.uid)
                {
                    d1.resolve();
                    d2.resolve();
                    d3.resolve();
                    return;
                }
                var $link = self.$el.find('.support_branding_link');
                ir_config_parameter.call(
                    'get_param', ['support_branding.company_name'])
                    .then(function(name)
                    {
                        $link.text(name);
                        d1.resolve();
                    });
                ir_config_parameter.call(
                    'get_param', ['support_branding.company_color'])
                    .then(function(color)
                    {
                        $link.css('color', color);
                        d2.resolve();
                    });
                ir_config_parameter.call(
                    'get_param', ['support_branding.company_url'])
                    .then(function(url)
                    {
                        $link.attr('href', url);
                        d3.resolve();
                    });

            });
            return jQuery.when(d1, d2, d3);
        },
    });
};
