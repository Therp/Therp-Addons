# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2013 Therp BV (<http://therp.nl>).
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

{
    "name": "Separator visibility depending on view mode",
    "version": "6.1.1.0r1",
    "author": "Therp BV",
    "category": "Tools",
    "depends": ['web_mode_visibility'],
    "description": """
Use the following options keys on separator tags and other form widget
to hide them in either page or form mode:

- page_invisible
- form_invisible

Please note that you need to allow the use of the options dictionary
on separators in openobject-server/openerp/addons/base/rng/view.rng,
or you will get view validation errors in modules that try to use
this functionality:

--- openerp/addons/base/rng/view.rng2012-02-13 10:17:58 +0000
+++ openerp/addons/base/rng/view.rng2013-05-07 09:40:10 +0000
@@ -442,6 +442,7 @@
             <rng:optional><rng:attribute name="col"/></rng:optional>
             <rng:optional><rng:attribute name="select"/></rng:optional>
             <rng:optional><rng:attribute name="orientation"/></rng:optional>
+            <rng:optional><rng:attribute name="options"/></rng:optional>
             <rng:zeroOrMore>
                 <rng:choice>
                     <rng:ref name="separator"/>

You do not need this module to simply hide fields. This can be
done solely with the 'web_mode_visibility' module, without changes to the
rng file.

This module is compatible with OpenERP 6.1.
    """,
    'js': [
        'static/src/js/web_mode_visibility.js',
        ],
}
