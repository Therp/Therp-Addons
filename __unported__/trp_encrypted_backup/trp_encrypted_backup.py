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
from openerp.osv.orm import TransientModel,except_orm
from openerp.osv import fields
import subprocess
import os.path
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from openerp.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
import logging
import datetime

class trp_backup_wizard(TransientModel):
    _name='trp_backup.wizard'

    _columns={
            'messages': fields.text('Messages', readonly=True),
            }

    _defaults={
            'messages': 'Press "Do backup" to start the backup process',
            }
    
    _logger=logging.getLogger('trp_backup')

    def do_backup_wizard(self, cr, uid, ids, context=None):
        _, messages, _=self.do_backup(cr, uid)
        self.write(cr, uid, ids, {'messages': messages})

    def do_backup_cron(self, cr, uid, context=None):
        self.do_backup(cr, uid)

    def do_backup(self, cr, uid):
        params=self.pool.get('ir.config_parameter')
        publc_key_file=params.get_param(cr, uid, 'trp_backup.publickeyfile') 
        backup_dir=params.get_param(cr, uid, 'trp_backup.backupdirectory')
        messages=''
        success=False
        
        if not os.path.isfile(str(publc_key_file)):
            raise except_orm(_('Error'),_('You need to give a *public* key to encrypt your backup - %s is not suitable')%(publc_key_file))
        if not os.path.isdir(str(backup_dir)):
            raise except_orm(_('Error'),_('You need to give a directory to backup to'))

        outfile=os.path.join(backup_dir, cr.dbname+'_'+
                datetime.datetime.now().strftime(
                    DEFAULT_SERVER_DATETIME_FORMAT).replace(' ', '_'))

        self._logger.info(_('starting backup to %s')%outfile)

        backup_process=subprocess.Popen(['pg_dump', 
            '--format', 'custom',
            '--no-owner',
            cr.dbname], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        crypt_process=subprocess.Popen(['openssl', 
            'smime', '-encrypt', '-aes256', '-binary', '-outform', 'DEM',
                '-out', outfile,
                publc_key_file],
                stdin=backup_process.stdout,stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)
        output=crypt_process.communicate()

        if crypt_process.returncode==0:
            messages+=_('Sucessfully backed up to %s')%outfile
            success=True
        else:
            messages+=_('There was an error during backup:')+'\n'
            messages+=(output[0]+'\n') if output[0] else ''
            messages+=(output[1]+'\n') if output[1] else ''

        self._logger.info(messages)

        return success, messages, outfile
