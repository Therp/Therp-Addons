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
    'description': """Creates crypted backups of the database which can securely
    be placed on public servers.

    After installation, you need to do some initial configuration in Settings->
    Customization -> Low level objects -> System parameters.
    Fill in the path to your public key file in trp_backup.publickeyfile and the
    directory where your backups are to be places in trp_backup.backupdirectory

    Your keypair can be created by running
    openssl req -x509 -nodes -days 100000 -newkey rsa:2048  -keyout privatekey.pem  -out publickey.pem  -subj '/'

    To restore a backup, run
    openssl smime -decrypt -binary -inform DEM -in [backup file] -inkey privatekey.pem | pg_restore --clean --dbname=[database name]
    """,
    'author': 'Therp BV',
    'website': 'http://www.therp.nl',
    "category": "Tools",
    "depends": [],
    'init_xml': ['data/ir_config_parameter.xml', 'data/ir_cron.xml'],
    'update_xml': ['trp_encrypted_backup.xml'],
    'installable': True,
    'active': False,
    'certificate': '',
}
