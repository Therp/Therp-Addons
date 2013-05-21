/*

      Copyright (C) 2013 Therp BV
      License: GNU AFFERO GENERAL PUBLIC LICENSE
      Version 3 or any later version

*/

openerp.trp_web_export_exclude = function(openerp) {
    openerp.web.search.ExtendedSearchProposition.include({
        
        init: function(parent, fields) {
            /* 
               Do the work of super's init function all over again,
               taking the export_exclude key into account this time
            */
            this._super(parent, fields);
            this.fields = _(fields).chain()
                .map(function(val, key) {return _.extend({}, val, {'name': key}); })
                .filter(function(field){return (!(field.export_exclude)) && (typeof field.store === 'undefined' || field.store || field.fnct_search)})
                .sortBy(function(field) {return field.string;})
                .value();
            this.attrs = {_: _, fields: this.fields, selected: null};
        }
    });
};
