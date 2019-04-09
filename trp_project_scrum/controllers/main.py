# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers import main


class Website(main.Website):

    @http.route()
    def web_login(self, redirect=None, *args, **kwargs):
        response = super(Website, self).web_login(
            redirect=redirect, *args, **kwargs)
        if not redirect and request.params['login_success']:
            if request.env['res.users'].browse(request.uid).has_group(
                    'trp_project_scrum.external_scrum_users'):
                return http.redirect_with_hash(
                    '/web?' + request.httprequest.query_string)
        return response
