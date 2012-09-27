# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2011-2012 Therp BV (<http://therp.nl>) Tiny SPRL (<http://tiny.be>))
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Use a fixed matrix to edit x2x fields',
    'version': '1.0r46',
    'description': """
    Provides a fixed (no possibility to add/remove lines) matrix to edit 
    one2many fields (many2one and many2many are a future extension), with all 
    lines in edit mode to allow simple matrix-style input.
    The widget is called one2many_matrix.
    """,
    'author': 'Therp BV',
    'website': 'http://www.therp.nl',
    "category": "Tools",
    "depends": ['web'],
    'js': ['static/src/js/one2many_matrix.js'],
    'installable': True,
    'active': False,
    'certificate': '',
}
