try:
    from openerp.addons.override_import_xml_schema import overrides_view
    overrides_view.append('web_mode_visibility_separator/view.rng.xsl')
except:
    pass
