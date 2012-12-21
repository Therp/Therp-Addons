# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    "name" : "Backgrounds for rml reports",
    "version" : "0.1r67",
    "author" : "Therp BV",
    "category": 'Reporting',
    'complexity': "normal",
    "description": """

This module allows you to select a background image for various reports. In order to use
these, you will need to install the configuration module for the module you want to use,
such as 

    trp_report_background_invoice
    trp_report_background_sale

You can add a selection of background images, and optionally associate them with a company.
Most likely, you will want to set a default background image per company.

Go to Settings -> Customizations -> Reports -> Report backgrounds to configure the actual background
images. The background images need to cover the full paper size.

To make these images appear in your reports, go to Settings -> Customizations -> Reports ->
Background configurations and click the 'Insert RML tags' button on the Invoice report background
configuration.

To display the background on other reports, you can easily create a simple configuration module. See
trp_report_background_sale for example.
    """,
    'website': 'http://therp.nl',
    'images' : [],
    'depends' : ['account'],
    'data': [
        'view/report_background.xml',
        'view/report_background_config.xml',
        'security/ir.model.access.csv',
        ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
