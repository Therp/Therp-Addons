# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, an open source suite of business apps
#    This module copyright (C) 2015 Therp BV (<http://therp.nl>).
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
    "name": "Dutch chart of accounts - autoinstall",
    "version": "1.0",
    "author": "Therp BV",
    "category": 'Accounting & Finance',
    'website': 'http://therp.nl',
    'depends': ['l10n_nl'],
    'data': [
        'data/configure_accounting.xml',
    ],
    "license": 'AGPL-3',
}
