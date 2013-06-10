/*

      Copyright (C) 2013 Therp BV
      License: GNU AFFERO GENERAL PUBLIC LICENSE
      Version 3 or any later version

*/

openerp.trp_extended_search_exclude = function(openerp) {
    openerp.web.SearchView.include({
        field_qualifies: function(field) {
            var complex_fields = {'one2many':0, 'many2one':0, 'many2many':0 };
            return (field.type in complex_fields && field.selectable && (!(field.export_exclude)));
        }
    });
};
