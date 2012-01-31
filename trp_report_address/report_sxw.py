from report.report_sxw import rml_parse, rml_parents, rml_tag

def display_address(self, address_browse_record, company=None):
    """
    Return a custom method to get a formatted address if displaying
    the country should be avoided in certain circumstances
    """
    
    if not company:
        return self.pool.get('res.partner.address')._display_address(
            self.cr, self.uid, address_browse_record)
    else:
        return self.pool.get('res.partner.address')._display_address_custom(
            self.cr, self.uid, address_browse_record, company)

# monkey patch the report object to accomodate our changes
rml_parse.display_address = display_address
