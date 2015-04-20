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

    instance.web.Session.include({
        session_authenticate: function()
        {
            var self = this;
            return this._super.apply(this, arguments)
            .then(function()
            {
                return self.setup_branding()
            });
        },
        session_init: function()
        {
            var self = this;
            return this._super.apply(this, arguments)
            .then(function()
            {
                return self.setup_branding()
            });
        },
        setup_branding: function()
        {
            var self = this,
                ir_config_parameter = new instance.web.Model('ir.config_parameter');
            if(!self.uid)
            {
                return jQuery.when();
            };
            return (new instance.web.Model('ir.config_parameter'))
                .query(['key', 'value'])
                .filter([
                    [
                        'key', 'in', [
                            'support_branding.support_email',
                            'support_branding.company_name',
                            'support_branding.company_color',
                            'support_branding.company_url',
                        ],
                    ]
                ])
                .all()
                .then(function(branding_values)
                {
                    _.each(branding_values, function(record)
                    {
                        self[record.key.replace('.', '_')] = record.value;
                    });
                });
        },
    });

    instance.web.CrashManager.include({
        show_error: function(error)
        {
            this._super.apply(this, arguments);
            jQuery('.support-branding-submit-form').each(function()
            {
                var $form = jQuery(this),
                    $button = $form.find('button');
                if(instance.client.session.support_branding_support_email)
                {
                    $form.attr(
                        'action',
                        'mailto:' + instance.client.session.support_branding_support_email);
                }
                if(instance.client.session.support_branding_company_name)
                {
                    $button.text(
                        _.str.sprintf(
                            instance.web._t('Email to %s'),
                            instance.client.session.support_branding_company_name));
                }
                $form.prependTo(
                    $form.parents('.ui-dialog').find('.ui-dialog-buttonpane'));
            });
        }
    });

    instance.web.WebClient.include({
        show_application: function()
        {
            var self = this;
            return jQuery.when(this._super(this, arguments))
            .then(function()
            {
                var $link = self.$el.find('.support_branding_link');
                $link.text(instance.client.session.support_branding_company_name);
                $link.css('color', instance.client.session.support_branding_company_color);
                $link.attr('href', instance.client.session.support_branding_company_url);
            });
        },
    });
};
