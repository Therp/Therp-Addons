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
import subprocess
from openerp.tools.translate import _

class trp_backup_wizard(TransientModel):
    _inherit='trp_backup.wizard'

    def do_backup(self, cr, uid):
        success, messages, backup_file=super(trp_backup_wizard, self).do_backup(cr, 
                uid)

        if success:
            messages+='\n'
            params=self.pool.get('ir.config_parameter')
            rsync_host=self.pool.get('ir.config_parameter').get_param(cr, uid, 
                    'trp_backup_rsync.host')
            
            self._logger.info(_('copying %s to %s')%(backup_file,rsync_host))
            
            run_transfer=True
            while run_transfer:
                rsync_process=subprocess.Popen(['rsync', 
                    '--partial',
                    backup_file,
                    rsync_host], 
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                output=rsync_process.communicate()
                
                if rsync_process.returncode==0:
                    messages+=_('Sucessfully copied %s to %s')%(backup_file,
                            rsync_host)
                    messages+=(output[0]+'\n') if output[0] else ''
                    messages+=(output[1]+'\n') if output[1] else ''
                    run_transfer=False
                else:
                    messages+=_('There was an error during transfer:')+'\n'
                    messages+=(output[0]+'\n') if output[0] else ''
                    messages+=(output[1]+'\n') if output[1] else ''
                    if rsync_process.returncode not in [23,30,35]:
                        run_transfer=False
                    
                self._logger.info(messages)
        else:
            self._logger(_('Backup failed, not running transfer'))

        return success, messages, backup_file
