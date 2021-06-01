# -*- coding: utf-8 -*-
# Code snippets from openobject-server 6.1:
#     Copyright 2004-2012 OpenERP S.A. <http://openerp.com>.
# Copyright 2013-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# pylint: disable=invalid-name
"""Make it possible to extend view.rng for validity check."""
import os
import logging
from lxml import etree

from openerp.osv.orm import Model
from openerp import tools

overrides_view = []

_logger = logging.getLogger(__name__)


class ir_ui_view(Model):
    _inherit = 'ir.ui.view'

    def _check_xml(self, cr, uid, ids, context=None):
        """Replace original function with patch that applies overrides."""
        for view in self.browse(cr, uid, ids, context):
            eview = etree.fromstring(view.arch.encode('utf8'))
            frng = tools.file_open(os.path.join('base', 'rng', 'view.rng'))
            try:
                relaxng_doc = etree.parse(frng)
                #  local change
                for override in overrides_view:
                    _logger.debug('loading override %s', override)
                    transformation = etree.XSLT(etree.parse(tools.file_open(override)))
                    relaxng_doc = transformation(relaxng_doc)
                #  _logger.debug(relaxng_doc)
                #  /local change
                try:
                    relaxng = etree.RelaxNG(relaxng_doc)
                    if not relaxng.validate(eview):
                        for error in relaxng.error_log:
                            _logger.error(tools.ustr(error))
                        return False
                except Exception:  # pylint: disable=broad-except
                    _logger.exception("Cannot load view validator")
                    return True  # Assume view is in order...
            finally:
                frng.close()
        return True

    #  pick up right reference for the constraint
    _constraints = [(_check_xml, 'Invalid XML for View Architecture!', ['arch'])]
