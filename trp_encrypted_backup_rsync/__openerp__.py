# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2011-2012 Therp BV (<http://therp.nl>)
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
    'name': 'backup',
    'version': '1.0',
    'description': """Allows you to copy your backup to a server supported by rsync
    Before being able to use it, fill in trp_backup_rsync.host via Settings->
    Customization -> Low level objects -> System parameters.

    This can be any host string supported by rsync, ie [USER@]HOST:DEST

    Note that the transfer will be restarted until it succeeds, so misconfiguration
    can lead to a dead lock.
    """,
    'author': 'Therp BV',
    'website': 'http://www.therp.nl',
    "category": "Tools",
    "depends": ['trp_encrypted_backup'],
    'init_xml': ['data/ir_config_parameter.xml'],
    'installable': True,
    'active': False,
    'certificate': '',
}
