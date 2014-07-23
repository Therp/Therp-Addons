openerp.trp_saved_selection = function(openerp) {

    _t = openerp.web._t

    // selection other properties of view in order to preserve
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

    keys = getKeys(openerp.web.Header);
    openerp.web.Header = openerp.web.Header.extend({
        on_selection_action: function() {
            // Call the default action on the model in the user's
            // saved selection and apply the domain
            var self = this;
            var dataset = new openerp.web.DataSet(this, "saved_selection.selection",
                                                  this.session.user_context);
            dataset.call_and_eval(
                'action_get', 
                [this.session.user_context],
                null,
                1,
                function(action) {
                    if (action) {
                        self.widget_parent.action_manager.do_action(action);
                    }
                    else {
                        alert(_t("Saved selection may not be initialized yet."));
                    }
                }
            );
        },

        on_selection_init: function() {
            // TODO: call the initialization wizard (cf. user's pref)
            var self = this;
            var dataset = new openerp.web.DataSet(this, "saved_selection.selection",
                                                  this.session.user_context);
            dataset.call_and_eval(
                'selection_init', 
                [this.session.user_context],
                null,
                1,
                function(action) {
                    self.widget_parent.action_manager.do_action(action);
                }
            );
        },

        do_update: function() {
            // Add hooks for interface buttons
            var self = this;
            this._super();
            var fct = function() {
                if (!self.session.uid) return;
                self.$element.find(".selection_action").click(self.on_selection_action);
                self.$element.find(".selection_init").click(self.on_selection_init);
            }
            this.update_promise = this.update_promise.pipe(fct, fct);
        },
    });
    // reselection other properties of the view
    setKeys(openerp.web.Header, keys);

    keys = getKeys(openerp.web.ListView);
    openerp.web.ListView = openerp.web.ListView.extend({

        update_saved_selection: function(mode, ids, domain) {
            /* 
               Connect to the server and update the user's selection selection.
               If we are in the selection selection itself, update the domain
               and trigger a reload of the records.
               For this purpose, the selection selection's action contains
               a custom attribute, 'is_saved_selection'.
            */

            var self = this;
            var rdataset = new openerp.web.DataSetStatic(self, "saved_selection.selection");
            // Request back a list of ids in the selection selection?
            var pass_ids = typeof(
                self.widget_parent.action.is_saved_selection) !== 'undefined'
            res = rdataset.call(
                "update", 
                [   self.widget_parent.dataset.model,
                    mode, ids, domain, pass_ids, this.session.user_context,
                ], 
                function(result) {
                    self.do_notify(openerp.web._t("Update saved selection"), result[0]);
                    if (self.widget_parent.action.is_saved_selection && result[1]) {
                        self.widget_parent.action.domain = [['id', 'in', result[1]]];
                        if (self.widget_parent.searchview) {
                            self.widget_parent.searchview.do_search();
                        }
                    }
                });
        },

        // Handle various operations on the user's selection selection
        on_sidebar_add_saved_selection: function() {
            this.update_saved_selection("add", this.groups.get_selection().ids, this.dataset.domain);
        },
        on_sidebar_del_saved_selection: function() {
	    // TODO: update the domain if we are in the selection selection view itself and refresh list
            this.update_saved_selection("delete", this.groups.get_selection().ids, this.dataset.domain);
        },
        on_sidebar_intersect_saved_selection: function() {
            this.update_saved_selection("intersect", this.groups.get_selection().ids, this.dataset.domain);
        },

        // Add operations for mutations on the saved selection
        on_loaded: function(data, grouped) {
            var self = this;
            this._super(data, grouped);
            if ((this.sidebar) && (!(this.sidebar.sections.saved_selection))) {
                this.sidebar.add_section(_t('Saved Selection'), 'saved_selection');
                this.sidebar.add_items('saved_selection', [
                    {
                        label: _t("Add"),
                        callback: self.on_sidebar_add_saved_selection
                    },
                    {
                        label: _t("Delete"),
                        callback: self.on_sidebar_del_saved_selection
                    },
                    {
                        label: _t("Intersection"),
                        callback: self.on_sidebar_intersect_saved_selection
                    },
                ]);
            }
        },
    });
    // reselection other properties of the ListView
    setKeys(openerp.web.ListView, keys);
}

