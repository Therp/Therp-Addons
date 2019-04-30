# -*- coding: utf-8 -*-
# © 2015 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def pre_init_hook(cr):
    cr.execute(
        """insert into ir_model_data
        (
            module, name, model,
            res_id, noupdate, date_update, date_init
        )
        select
        'dead_mans_switch_therp', 'config_parameter', 'ir.config_parameter',
        id, False, write_date, create_date
        from ir_config_parameter
        where key='dead_mans_switch_client.url'
        """
    )
