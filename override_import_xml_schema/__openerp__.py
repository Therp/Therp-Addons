# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>)
#    All Rights Reserved
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
    'name': 'Convenient way to override import_xml.rng and view.rng',
    'version': '1.0',
    'description': """This addon allows you to override import_xml.rng and
    view.rng in a clean way that also can coexist with multiple changes from
    multiple addons.


    USAGE:
    ------
    Depend on this addon.

    Then in your __init__.py:
    from openerp.addons.override_import_xml_schema import overrides
    overrides.append(
        '[name of your module]/[filename relative to module's root]')
    or for views import overrides_view

    In your override xml, start with the identity transformation
    http://en.wikipedia.org/wiki/Identity_transform#Using_XSLT
    and then change the tree as needed.

    Have a look at the example module included, it demonstrate how to add
    allowed attributes.
    """,
    'author': ['Therp BV', 'OpenERP SA'],
    'website': 'http://www.therp.nl',
    "category": "Dependency",
    "depends": [
        'base',
        ],
    'css': [
        ],
    'data': [
        ],
    'js': [
        ],
    'installable': True,
    'active': False,
    'certificate': '',
}
