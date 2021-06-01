# -*- coding: utf-8 -*-
# Code snippets from openobject-server 6.1:
#     Copyright 2004-2012 OpenERP S.A. <http://openerp.com>.
# Copyright 2013-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""dd posibility for new elements/attributes in xml import."""
# pylint: disable=invalid-name,too-many-arguments
import os
import logging

from lxml import etree

from openerp.tools import xml_import, config, misc
from openerp import tools

_logger = logging.getLogger(__name__)

overrides = []

original_convert_xml_import = tools.convert_xml_import


def convert_xml_import(
        cr, module, xmlfile, idref=None, mode='init', noupdate=False, report=None):
    '''
    Copy of openerp.tools.convert_xml_import save for the xml transformation
    part
    '''
    doc = etree.parse(xmlfile)
    # local change
    relaxng = etree.parse(os.path.join(config['root_path'], 'import_xml.rng'))
    for override in overrides:
        _logger.debug('applying override %s', str(overrides))
        transformation = etree.XSLT(etree.parse(tools.file_open(override)))
        relaxng = transformation(relaxng)
        _logger.debug('succeeded')
    try:
        relaxng = etree.RelaxNG(relaxng)
    # /local change
        relaxng.assert_(doc)
    except Exception:
        _logger.error('The XML file does not fit the required schema !')
        _logger.error(misc.ustr(relaxng.error_log.last_error))
        raise

    if idref is None:
        idref = {}
    obj = xml_import(cr, module, idref, mode, report=report, noupdate=noupdate)
    obj.parse(doc.getroot())
    return True


tools.convert_xml_import = convert_xml_import
