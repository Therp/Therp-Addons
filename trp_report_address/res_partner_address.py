# -*- coding: utf-8 -*-
from osv import osv, fields

class res_partner_address(osv.osv):
    _inherit = 'res.partner.address'

    def _display_address_custom(self, cr, uid, address, company, context=None):
        '''
        This method is almost identical to the one in base/res/res_partner.py,
        but it does not print the country if this is equal to the company partner's
        country, unless we print the company partner's own address.

        Note that this method has a different signature than the original one,
        as it passes the company browse record.

        :param address: browse record of the res.partner.address to format
        :param company: browse record of the res.company
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''
        # get the address format
        address_format = address.country_id and address.country_id.address_format or \
                                         '%(street)s\n%(street2)s\n%(city)s,%(state_code)s %(zip)s' 
        # get the information that will be injected into the display format
        args = {
            'state_code': address.state_id and address.state_id.code or '',
            'state_name': address.state_id and address.state_id.name or '',
            'country_code': address.country_id and address.country_id.code or '',
            'country_name': address.country_id and address.country_id.name or '',
        }


        # custom changes here
        if (address.country_id and company and company.partner_id.country and 
            company.partner_id.country.id ==  address.country_id.id and
            not (address.partner_id and 
                 address.partner_id.id == company.partner_id.id)
            ):
            args['country_name'] = ''
        # end of custom changes

        address_field = ['title', 'street', 'street2', 'zip', 'city']
        for field in address_field :
            args[field] = getattr(address, field) or ''

        return address_format % args

res_partner_address()
