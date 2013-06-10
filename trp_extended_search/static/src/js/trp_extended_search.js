/*---------------------------------------------------------
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

Collect *many* fields in a dropdown in the regular search view
Upon selection of a field in this dropdown, inject an embedded search view in a regular search view.
Upon submit of the regular search view, collect the domain from the embedded search view and apply using normal dot notation
Collect domain from advanced filters from subsearchviews
Upon clear of the regular search view, reset the embedded search views
Button minimize on the embedded search view -> fold or unfold the embedded search view
Button close on the embedded search view -> remove the embedded search view
Collect subselections when saving a filter on the main search view
Do not display clear and submit button button for embedded searches
Remove additional filter options from embedded search forms
  (will this fix the default action on [enter] key?)

Possible future improvements
- Merge extended search dropdown with filter dropdown
- replace subsearches array by widget_children logic (may not be feasible)
- Hide useless Group by buttons in embedded search views

 *---------------------------------------------------------*/

openerp.trp_extended_search = function(openerp) {

    // store other properties of view in order to preserve
    // dot notation on the view itself
    // (e.g. ListView.Groups, ListView.List in case of ListView)
    var getKeys = function(obj){
        var keys = {};
        for(var key in obj){
            // Should not be necessary anymore
            // since using setKeys
            if (key != 'constructor' &&
                key != 'extend' &&
                key != 'include') {
                keys[key] = obj[key];
            }
        }
        return keys;
    }

    var setKeys = function(obj, keys) {
        for (var key in keys) {
            if (! obj[key]) {
                obj[key] = keys[key]; 
            }
        }
    }

    var QWeb = openerp.web.qweb;
    
    openerp.web.TrpExtendedSearch = openerp.web.Widget.extend({
	/*

	  A container widget for the embedded search form 
	  that adds a label and a close button
	  
	*/
	template: "TrpExtendedSearch.view",
	make_id: function () {
            this.element_id = _.uniqueId(
		['search'].concat(
                    _.compact(_.toArray(arguments)),
                    ['']).join('_'));
            return this.element_id;
	},

	init: function(parent, field, relation, string) {
	    this._super(parent);
	    this.string = string;
	    this.parent = parent;
	    this.make_id('extended');
	    this.subsearch = null;

            // create the subsearch widget
	    var dataset = new openerp.web.DataSetSearch(this, relation, {}, []);
	    this.subsearch = new openerp.web.SearchView(this, dataset, false, {});
	    // Set the correct domain_base and indentation level
	    this.subsearch.domain_base = parent.domain_base + field + '.';
	},

	start: function() {
            // append the subsearch widget to the container
	    this.subsearch.appendTo(this.$element.find(
                'div.trp_extendedsearch_content'));
	    var self = this;
            // stop when delete is clicked
	    this.$element.find('.trp_extended_search_delete_prop').click(
                function () {
		    self.stop();
                });
	},

	stop: function() {
	    var self = this;
            // remove the container from the parent's list
	    this.parent.subsearch_containers = jQuery.grep(
                self.parent.subsearch_containers, function(value) {
		return value != self;
	    });
	    this.subsearch.stop();
	    this._super();
	},
    }),
    
    openerp.web.SearchView = openerp.web.SearchView.extend({
        filter_items: function(items) {
            /* 
               Prevent filter buttons from showing up.
               Also remove groups that were left empty as a result of
               removing the filter buttons.
            */
            var new_items = [];
            var len=items.length;
            for(var i=0; i<len; i++) {
                var item = items[i];
                if (item.tag == 'group') {
                    item.children = this.filter_items(item.children);
                    if (item.children.length) {
                        new_items.push(item);
                    }
                }
                else if (item.tag != 'filter') {
                    new_items.push(item);
                }
            }
            return new_items;
        },
            
        make_widgets: function(items, fields) {
            /* 
               For now, remove filter buttons from the embedded 
               search forms. The domain expressions can not
               easily be prefixed by the subsearch's domain_base
               expression.
            */
            if (this.domain_base) {
                items = this.filter_items(items);
            }
            return this._super(items, fields);
        },

	build_search_data: function() {
	    /* 
	       
	       Collect the domains from the subselection
	       
	    */
	    
	    result = this._super();
	    var domains = result['domains'];
	    _.each(this.subsearch_containers, function(container) {
		subresult = container.subsearch.build_search_data();
		_.each(subresult['domains'], function(domain) {
		    domains.push(domain);
		});
	    });
	    result['domains'] = domains;
	    return result;
	},
	
    	do_clear: function() {
	    /* 
               How are simple fields being cleared anyway?
	       Completely remove subsearch widgets instead.
	    */
	    _.each(this.subsearch_containers, function(container) {
		container.stop();
	    });
	    return this._super();
	},
	
	stop: function() {
	    this._super();
	    _.each(this.subsearch_containers, function(container) {
		container.stop();
	    });
	},

	strcmp: function (str1, str2) {
	    // http://kevin.vanzonneveld.net
	    return ( ( str1 == str2 ) ? 0 : ( ( str1 > str2 ) ? 1 : -1 ) );
	},

        filter_filters: function(nodeset) {
            var self = this;
            var nodes_remove = []
            _.each(nodeset, function(node) {
                if (node.nodeName == 'OPTGROUP') {
                    self.filter_filters(node.children);
                    if (! node.children.length) {
                        nodes_remove.push(node);
                    }
                }
                else if (node && node.nodeName == 'OPTION') {
                    if (node.value == 'manage_filters' ||
                        node.value == 'add_to_dashboard' ||
                        node.value == 'save_filter') {
                        nodes_remove.push(node);
                    }
                }
            });
            while (nodes_remove.length) {
                var node = nodes_remove.pop();
                node.parentNode.removeChild(node);
            }
        },

        reload_managed_filters: function() {
            /* filter out various options 
               if embedded 
            */
            var self = this;
            res = this._super();
            res = res.then(function(result) {
                if (self.domain_base) {
                    var nodeset = $(self.$element.find(
                        'select.oe_search-view-filters-management'
                    )).children();
                    self.filter_filters(nodeset);
                }
            });
            return res;
        },

        field_qualifies: function(field) {
            var complex_fields = {'one2many':0, 'many2one':0, 'many2many':0 };
            return (field.type in complex_fields && field.selectable);
        },
            
        find_top: function(search_view) {
            /*
               Retrieve the primary search view
            */
            if (search_view.widget_parent && search_view.widget_parent.parent) {
                return this.find_top(search_view.widget_parent.parent);
            }
            return search_view;
        },

	configure_subsearch: function() {
	    /*
              hide the search and clear buttons, if embedded
            */
            if (this.domain_base) {
                $(this.$element.find('button.oe_button')).hide();
            }

            /* 
               Restore default submit action of the form, 
               which is the Search button of the primary search view
            */
            var top = this.find_top(this);
            top.$element.find('form').submit(top.do_search);

	    /* 
	       Replace the id with a traceble one.
	       Could not get Qweb to do this for me for some reason
	    */
	    $(this.$element.find('div.trp_searchview_extended_search')).attr(
		'id', this.element_id + '_trp_extended_search');
	    
	    var self = this;
	    /*
	      
	      There is no link from the search fields to the SearchView
	      so we add it here for every input, in order to query
	      the domain_base.
	      
	    */
	    _.each(self.inputs, function (input) {
		input.parent = self;
	    });
	    /* 
	       
	       We are looking for these kinds of fields.
	       Create an array with dummy values to be able to use the 'in'
	       operator, which does not work on a simple list.
	       
	    */
	    var extendedsearch = this.$element.find(".oe_search-view-extended-select");
	    
	    this.rpc("/web/searchview/fields_get",
		     {"model": this.model}, function(data) {
			 var fields = {};
			 var field_list = [];
			 var sort_fields = data.fields;
			 _.each(data.fields, function(field, key) {
			     if (self.field_qualifies(field)) {
				 self.xsfields[key] = field;
				 field['name'] = key;
				 field_list.push(field);
			     }
			 });
			 field_list.sort(function(a, b) {
			     return self.strcmp(a['string'], b['string']) });
			 extendedsearch.html(QWeb.render("SearchView.extended-select", {fields: field_list }));
		     }
		    );
	    this.$element.find('.oe_search-view-extended-select').change(function() {
		self.xschanged();
	    });
	},
	
	init: function(parent, dataset, view_id, defaults) {
	    this._super(parent, dataset, view_id, defaults);
	    
	    // Do some bookkeeping
	    this.domain_base = '';
	    this.subsearch_containers = []
	    this.xsfields = {}; // list of relation fields on the model
	    
	    this.on_loaded.add_last(_.bind(this.configure_subsearch, this));
	},
	
        xschanged: function() {
	    /* 
	       
	       When a field in the dropdown has been selected, a subselection 
	       is loaded in a container below the main search view
	       
	    */
	    var select = this.$element.find(".oe_search-view-extended-select")
	    var val = select.val();
	    if (val.slice(0,1) != "_") {
                subsearch_container = new openerp.web.TrpExtendedSearch(
                    this, val, this.xsfields[val].relation,
                    this.xsfields[val].string);
		subsearch_container.appendTo(
                    this.$element.find(
                        '#' + this.element_id + '_trp_extended_search')
                );
		this.subsearch_containers.push(subsearch_container)
	    }
	    // Reset the dropdown
	    select.val("_extendedselect");
	},
    });
    
    /* 
       Prefix the domain_base to field names in calls to make_domain() 
       for every field type.

       TODO: handle filter buttons domains, such as
       
       [('perm_read', '=',True),('perm_write','=',True),
        ('perm_create','=',True),('perm_unlink','=',True)]
        
        and
         
        ['!', ('category_id.parent_id','child_of','Hidden')]

       It *looks* like we can prefix the
       first argument of every triple.

       For now, filter buttons are removed from the subsearch view.
       (see make_widgets())

    */
    openerp.web.search.CharField = openerp.web.search.CharField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.NumberField = openerp.web.search.NumberField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.IntegerField = openerp.web.search.IntegerField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.FloatField = openerp.web.search.FloatField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.SelectionField = openerp.web.search.SelectionField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.Field = openerp.web.search.Field.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.DateTimeField = openerp.web.search.DateTimeField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.DateField = openerp.web.search.DateField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.ManyToOneField = openerp.web.search.ManyToOneField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    openerp.web.search.BooleanField = openerp.web.search.BooleanField.extend({
	make_domain: function(name, operator, value) {
	    return this._super(this.parent.domain_base + name, operator, value);
	},
    });
    
    /*
      
      Store the namespace references before extending a subpath,
      otherwise, these paths cannot be resolved in core.js:get_object().
      Surely, this can be solved more elegantly (Reply to self: 
      yes, see trp_selection_store_web).
      
    */

    keys = getKeys(openerp.web.search.ExtendedSearchProposition)
    openerp.web.search.ExtendedSearchProposition = openerp.web.search.ExtendedSearchProposition.extend({
    	get_proposition: function() {
	    /*
	      
	      Prefix the domain_base to advanced filters of subselections.
	      This is safe, because the original function always returns 
	      
	      [fieldname, operator, value]
	      
   	      (as long as it returns a non-false value). See search.js#1096.
	      
	    */
    	    result = this._super();
	    if (result) {
		/* 
		   
		   Apparently, we have to traverse the widgets and objects as follows,
		   in order to arrive at the SearchView:
		   ExtendedSearchProposition <- ExtendedSearchGroup <- ExtendedSearch <- SearchView
		   It sure looks like a hack...
		   
		*/
		result[0] = this.widget_parent.widget_parent.parent.domain_base + result[0];
	    }
	    return result;
	},
    });
    
    // restore the namespace references in the registry
    setKeys(openerp.web.search.ExtendedSearchProposition, keys);

};
