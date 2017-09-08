odoo.define('cms_rights.website_template_pages', function (require) {
'use strict';

var Model = require('web.Model');
var ajax = require('web.ajax');
var core = require('web.core');
var base = require('web_editor.base');
var web_editor = require('web_editor.editor');
var options = require('web_editor.snippets.options');
var snippet_editor = require('web_editor.snippet.editor');
var session = require('web.session');
var website = require('website.website');
var _t = core._t;
var Widget = require('web.Widget');
var contentMenu = require('website.contentMenu');
var qweb = core.qweb;

ajax.loadXML('/cms_rights/static/src/xml/website_template_pages.xml', qweb);

    contentMenu.TopBar.include({
        new_webpage: function() {

    		var self = this;

    		this.template = 'cms_rights.pick_template_modal';
    		self.$modal = $( qweb.render(this.template, {}) );

    		$('body').append(self.$modal);

			session.rpc('/template/pages', {}).then(function(result) {
			    self.$modal.find("#templates_div").html(result.html_string)
            });

            $('#oe_webpage_template_modal').modal('show');

            $('body').on('click', '.page_template_glass_overlay', function() {
			    var page_template = $(this).data('template');

                //Deselect the cuurent one
                $(".page_template_glass_overlay").removeClass("page_template_glass_overlay_selected");

                $(this).addClass('page_template_glass_overlay_selected');
                $("#selected_template_id").val(page_template);

            });

            $('body').on('click', '#submit_webpage_template', function() {
                var page_name = false;
			    var page_template = $("#selected_template_id").val();
                var page_url = $("#page_url").val();
			    page_name = $("#page_title").val();
                if (page_name){
                    var url = '/template/pages/new' + encodeURIComponent(page_name);
    				session.rpc('/template/pages/new', {'template_id': page_template, 'page_name': page_name, 'url': page_url}).then(function(result) {
    				    //redirect to new page
    					window.location.href = "/page/" + result.page_name;
    				});
                }
                else{
                    alert("Please enter a Page Title");
                   $("#page_title").parents(".form-group").addClass('has-error');
                }

            });

        },
        save_webpage: function() {
            var view_id = $(document.documentElement).data('view-xmlid');
			session.rpc('/template/pages/save', {'view_id': view_id}).then(function(result) {
			    if (result.code == "good") {
				    alert("Template Saved");
			    }
			});

	    },
    });


});
