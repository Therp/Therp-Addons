# -*- coding: utf-8 -*-
# Copyright 2016-2018 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Configure scheduler_error_mailer for Therp",
    "version": "10.0.1.0.0",
    "author": "Therp BV",
    "license": "AGPL-3",
    "category": "Extra Tools",
    "summary": "Provides a default template for all cronjobs",
    "depends": ["scheduler_error_mailer"],
    "data": ["data/mail_template.xml"],
    "post_init_hook": "post_init_hook",
}
