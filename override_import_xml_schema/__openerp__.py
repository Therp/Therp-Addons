# -*- coding: utf-8 -*-
# Copyright 2013-2021 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Convenient way to override import_xml.rng and view.rng',
    'version': '6.1.1.0.0',
    'description': """This addon allows you to override import_xml.rng and
    view.rng in a clean way that also can coexist with multiple changes from
    multiple addons.

    DEPRECATED:
    - We now use a modified ocb-server repository that has the needed changes
      already applied to the base view.rng.

    USAGE:
    ------
    Depend on this addon.

    Then in your __init__.py:
    from openerp.addons.override_import_xml_schema import overrides
    overrides.append(
        '[name of your module]/[filename relative to module's root]')
    or for views import overrides_view

    In your override xml, start with the identity transformation
    http://en.wikipedia.org/wiki/Identity_transform#Using_XSLT
    and then change the tree as needed.

    Have a look at the example module included, it demonstrate how to add
    allowed attributes.
    """,
    'author': ['Therp BV', 'OpenERP SA'],
    'website': 'http://www.therp.nl',
    "category": "Dependency",
    "depends": [
        'base',
        ],
    'installable': True,
    'active': False,
    'certificate': '',
}
