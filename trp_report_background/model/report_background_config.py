# # -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2012 Therp BV (<http://therp.nl>).
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

import os
from xml.etree import ElementTree
from osv import fields, osv
from tools.translate import _
from openerp.modules import get_module_path

IMAGETAG="<image x=\"0cm\" y=\"0.0cm\" height=\"29.7cm\" >[[ o.report_background_id.image and o.report_background_id.image or removeParentNode('image') ]]</image>"

class report_background_config(osv.osv):
    _name = 'report.background.config'
    _description = 'Report background configuration'
    _columns = {
        'name': fields.char('Name', size=64, required=True),
        'report_id': fields.many2one('ir.actions.report.xml', 'XML Report'),
        }

    def insert(self, cr, uid, ids, context=None):
        report_pool = self.pool.get('ir.actions.report.xml')

        def get_report_path(report_rml):
            path_parts = report_rml.split('/')
            module_path = get_module_path(path_parts[0])
            return os.sep.join([module_path] + path_parts[1:])
            
        def get_tree(report):
            """
            Retrieve the XML data from file or from the database

            @report: xml report browse record
            """
            if report['report_rml']:
                document = ElementTree.parse(
                    get_report_path(report['report_rml']))
            elif report['report_rml_content_data']:
                document = ElementTree.fromstring(
                    report['report_rml_content_data'])
            else:
                osv.except_osv(
                    _('Error'),
                    _('No rml content found in report %s') % report['name'])
            return document

        def store_tree(report, tree):
            """
            Store the modified XML data on file or in the database

            @report: xml report browse record
            @tree: etree parsed xml structure
            """
            document_string = "%s\n%s" % (
                '<?xml version="1.0"?>',
                ElementTree.tostring(tree.getroot())
                )
            if report['report_rml']:
                output_file = open(
                    get_report_path(report['report_rml']), 'w')
                output_file.write(document_string)
                output_file.close()
            else:
                report_pool.write(
                    cr, uid, report['id'], {
                        'report_rml_content_data': document_string,
                        },
                    context=context)

        def insert_background_node(tree):
            """
            Remove all image tags from the header,
            then insert our own.

            @tree: etree parsed xml structure
            """
            imagenode = ElementTree.fromstring(IMAGETAG)
            for template in tree.findall(
                './template/pageTemplate'):
                pagegraphics = template.find(
                    './pageGraphics')
                if not pagegraphics:
                    pagegraphics = ElementTree.SubElement(
                        template, 'pageGraphics')
                for node in pagegraphics.findall('./image'):
                    # remove any existing image tags
                    pagegraphics.remove(node)
                pagegraphics.append(imagenode)

        report_ids = [x['report_id'][0] for x in self.read(
                cr, uid, ids, ['report_id'], context=context)]
        for report in report_pool.read(
            cr, uid, report_ids, context=context):
            tree = get_tree(report)
            insert_background_node(tree)
            store_tree(report, tree)

        # Disable company headers
        report_pool.write(cr, uid, report_ids, {
                'header': False}, context=context)
