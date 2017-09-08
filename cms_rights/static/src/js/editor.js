odoo.define('cms_rights.editor', function (require) {
"use strict";

var ajax = require('web.ajax');
var Model = require('web.Model');
var Widget = require('web.Widget');
var widget = require('web_editor.widget');
var core = require('web.core');
var base = require('web_editor.base');
var editor = require('web_editor.editor');
var rte = require('web_editor.rte');
var snippet = require('web_editor.snippet.editor');

var qweb = core.qweb;
var _t = core._t;

ajax.loadXML('/cms_rights/static/src/xml/editor.xml', qweb);

var toolbar = [
                ['style', ['style']],
                ['font', ['bold', 'italic', 'underline', 'clear']],
                ['insert', ['link', 'picture']],
                ['history', ['undo', 'redo']],
            ]
var method = 'save'
var Users = new Model('res.users');
Users.call('has_group', ['base.group_website_designer']).done(function(is_designer) {
    if (!is_designer) { 
        method = 'template_to_approve'
        toolbar = [
                    ['style', ['style']],
                    ['font', ['bold', 'italic', 'underline', 'clear']],
                    ['history', ['undo', 'redo']],
                ]
    }

});


rte.Class.include({
    // python method call on propose button click
	draft: function (context) {
        var self = this;
        this.__saved = {}; // list of allready saved views and data

        var editables = rte.history.getEditableHasUndo();

        var defs = $('.o_dirty')
            .removeAttr('contentEditable')
            .removeClass('o_dirty oe_carlos_danger o_is_inline_editable')
            .map(function () {
                var $el = $(this);

                $el.find('[class]').filter(function () {
                    if (!this.className.match(/\S/)) {
                        this.removeAttribute("class");
                    }
                });

                // TODO: Add a queue with concurrency limit in webclient
                // https://github.com/medikoo/deferred/blob/master/lib/ext/function/gate.js
                return self.saving_mutex.exec(function () {
                    return self.draftElement($el, context)
                        .then(undefined, function (thing, response) {
                            // because ckeditor regenerates all the dom,
                            // we can't just setup the popover here as
                            // everything will be destroyed by the DOM
                            // regeneration. Add markings instead, and
                            // returns a new rejection with all relevant
                            // info
                            var id = _.uniqueId('carlos_danger_');
                            $el.addClass('o_dirty oe_carlos_danger ' + id);
                            return $.Deferred().reject({
                                id: id,
                                error: response.data,
                            });
                        });
                });
            }).get();

        return $.when.apply(null, defs).then(function () {
            window.onbeforeunload = null;
        }, function (failed) {
            // If there were errors, re-enable edition
            self.stop();
            self.start();
            // jquery's deferred being a pain in the ass
            if (!_.isArray(failed)) { failed = [failed]; }

            _(failed).each(function (failure) {
                var html = failure.error.exception_type === "except_osv";
                if (html) {
                    var msg = $("<div/>").text(failure.error.message).html();
                    var data = msg.substring(3,msg.length-2).split(/', u'/);
                    failure.error.message = '<b>' + data[0] + '</b>' + data[1];
                }
                $('.o_editable.' + failure.id)
                    .removeClass(failure.id)
                    .popover({
                        html: html,
                        trigger: 'hover',
                        content: failure.error.message,
                        placement: 'auto top',
                    })
                    // Force-show popovers so users will notice them.
                    .popover('show');
            });
        });
    },
    
    draftElement: function ($el, context) {
        if ($el.data('oe-model')) {
            var key =  $el.data('oe-model')+":"+$el.data('oe-id')+":"+$el.data('oe-field')+":"+$el.data('oe-type')+":"+$el.data('oe-expression');
            if (this.__saved[key]) return true;
            this.__saved[key] = true;
        }
        var markup = this.getEscapedElement($el).prop('outerHTML');
        return ajax.jsonRpc('/web/dataset/call', 'call', {
            model: 'ir.ui.view',
            method: 'save_draft_template',
            args: [
                $el.data('oe-id'),
                markup,
                $el.data('oe-xpath') || null,
                _.omit(context || base.get_context(), 'lang')
            ],
        });
    },
    
	saveElement: function ($el, context) {
        if ($el.data('oe-model')) {
            var key =  $el.data('oe-model')+":"+$el.data('oe-id')+":"+$el.data('oe-field')+":"+$el.data('oe-type')+":"+$el.data('oe-expression');
            if (this.__saved[key]) return true;
            this.__saved[key] = true;
        }
        var markup = this.getEscapedElement($el).prop('outerHTML');
        return ajax.jsonRpc('/web/dataset/call', 'call', {
            model: 'ir.ui.view',
            method: method,
            args: [
                $el.data('oe-id'),
                markup,
                $el.data('oe-xpath') || null,
                _.omit(context || base.get_context(), 'lang')
            ],
        });
    },

    // restrict MMs to access font-size, font-color
    config: function ($editable) {
        return {
            'airMode' : true,
            'focus': false,
            'airPopover': toolbar,
            'styleWithSpan': false,
            'inlinemedia' : ['p'],
            'lang': "odoo",
            'onChange': function (html, $editable) {
                $editable.trigger("content_changed");
            }
        };
    },
});

editor.Class.include({
    events: {
    	'click button[data-action=save]': 'save',
        'click a[data-action=cancel]': 'cancel',
        'click button[data-action=propose]': 'propose',
    },
    start: function () {
    	self.$('button[data-action="propose"]').hide();
    	self.$('button[data-action="draft"]').hide();
    	var Users = new Model('res.users');
        Users.call('has_group', ['base.group_website_designer']).done(function(is_designer) {
            if (!is_designer) {self.$('button[data-action="save"]').hide();self.$('button[data-action="draft"]').show();self.$('button[data-action="propose"]').show();}
        });
        this.$('button[data-action="propose"]').prop('disabled', true);
        this.$('button[data-action="draft"]').prop('disabled', true);
    	return this._super();
    },
    rte_changed: function () {
    	this.$('button[data-action=draft]').prop('disabled', !rte.history.getEditableHasUndo().length);
    	this.$('button[data-action=propose]').prop('disabled', !rte.history.getEditableHasUndo().length);
        this.$('button[data-action=save]').prop('disabled', !rte.history.getEditableHasUndo().length);
    },
    draft: function () {
    	return this.rte.draft().then(function () {
            editor.reload();
        });
    },
    propose: function () {
    	return this.rte.save().then(function () {
    		$.session.set("propose_cookie", "propose_save");
            editor.reload();
        });
    },
});

if($.session.get("propose_cookie") == "propose_save"){
    $("#myModal").modal('show');
    $.session.remove('propose_cookie');
}

// prevent MMs to attach image on their own
widget.MediaDialog.include({
    start: function () {
        this._super();
        this.$("#editor-media-image").empty();
        this.$("#editor-media-document").empty();

        this.imageDialog = new ImageDialog(this, this.media, this.options);
        this.documentDialog = new ImageDialog(this, this.media, _.extend({'document': true}, this.options));
        this.documentDialog.appendTo(this.$("#editor-media-document"));

        this.active = this.imageDialog;

        $('a[data-toggle="tab"]').on('shown.bs.tab', function (event) {
            if ($(event.target).is('[href="#editor-media-image"]')) {
                self.active = self.imageDialog;
                self.$('li.search, li.previous, li.next').removeClass("hidden");
            } if ($(event.target).is('[href="#editor-media-document"]')) {
                self.active = self.documentDialog;
                self.$('li.search, li.previous, li.next').removeClass("hidden");
            }
        });     
    },

});

var IMAGES_PER_ROW = 6;
var IMAGES_ROWS = 2;
var ImageDialog = Widget.extend({
    template: 'web_editor.dialog.image',
    events: {
        'hidden.bs.modal': 'destroy',
        'keydown.dismiss.bs.modal': 'stop_escape',
        'click button.save': 'save',
        'click button[data-dismiss="modal"]': 'cancel',
        'change .url-source': function (e) {
            this.changed($(e.target));
        },
        'click button.filepicker': function () {
            var filepicker = this.$('input[type=file]');
            if (!_.isEmpty(filepicker)){
                filepicker[0].click();
            }
        },
        'click .js_disable_optimization': function () {
            this.$('input[name="disable_optimization"]').val('1');
            var filepicker = this.$('button.filepicker');
            if (!_.isEmpty(filepicker)){
                filepicker[0].click();
            }
        },
        'change input[type=file]': 'file_selection',
        'click .existing-attachments [data-src]': 'select_existing',
        'click .existing-attachment-remove': 'try_remove',
        'keydown.dismiss.bs.modal': function(){},
    },
    init: function (parent, media, options) {
        this._super();
        this.options = options || {};
        this.accept = this.options.accept || this.options.document ? "*/*" : "image/*";
        this.domain = this.options.domain || ['|', ['mimetype', '=', false], ['mimetype', this.options.document ? 'not in' : 'in', ['image/gif', 'image/jpe', 'image/jpeg', 'image/jpg', 'image/gif', 'image/png']]];
        this.parent = parent;
        this.old_media = media;
        this.media = media;
        this.images = [];
        this.page = 0;
    },
    start: function () {
        this.$preview = this.$('.preview-container').detach();
        var self = this;
        var res = this._super();
        var o = { url: null, alt: null };

        var Users = new Model('res.users');
        Users.call('has_group', ['base.group_website_designer']).done(function(is_designer) {
            if (!is_designer) {self.$('div[class="well"]').hide();}
        });

        if ($(this.media).is("img")) {
            o.url = this.media.getAttribute('src');
        } else if ($(this.media).is("a.o_image")) {
            o.url = this.media.getAttribute('href').replace(/[?].*/, '');
            o.id = +o.url.match(/\/web\/content\/([0-9]*)/, '')[1];
        }
        this.parent.$(".pager > li").click(function (e) {
            if(!self.$el.is(':visible')) {
                return;
            }
            e.preventDefault();
            var $target = $(e.currentTarget);
            if ($target.hasClass('disabled')) {
                return;
            }
            self.page += $target.hasClass('previous') ? -1 : 1;
            self.display_attachments();
        });
        this.fetch_existing().then(function () {
            self.set_image(_.find(self.records, function (record) { return record.url === o.url;}) || o);
        });
        return res;
    },
    push: function (attachment) {
        if (this.options.select_images) {
            if (img.length) {
                this.images.splice(this.images.indexOf(img[0]),1);
            }
        } else {
            this.images = [];
        }
        this.images.push(attachment);
    },
    save: function () {
        if (this.options.select_images) {
            this.parent.trigger("save", this.images);
            return this.images;
        }
        this.parent.trigger("save", this.media);

        var img = this.images[0];
        if (!img) {
            var id = this.$(".existing-attachments [data-src]:first").data('id');
            img = _.find(this.images, function (img) { return img.id === id;});
        }

        if (!img.is_document) {
            if (this.media.tagName !== "IMG" || !this.old_media) {
                this.add_class = "pull-left";
            }
            if(this.media.tagName !== "IMG") {
                var media = document.createElement('img');
                $(this.media).replaceWith(media);
            }
            this.media.setAttribute('src', img.src);
        } else {
            if (this.media.tagName !== "A") {
                $('.note-control-selection').hide();
                var media = document.createElement('a');
                this.media = media;
            }
            this.media.setAttribute('href', '/web/content/' + img.id + '?unique=' + img.checksum + '&download=true');
            $(this.media).addClass('o_image').attr('title', img.name).attr('data-mimetype', img.mimetype);
        }

        $(this.media).attr('alt', img.alt);
        var style = this.style;
        if (style) { $(this.media).css(style); }

        return this.media;
    },
    clear: function () {
        this.media.className = this.media.className.replace(/(^|\s+)((img(\s|$)|img-(?!circle|rounded|thumbnail))[^\s]*)/g, ' ');
    },
    cancel: function () {
        this.trigger('cancel');
    },
    change_input: function (e) {
        var $input = $(e.target);
        var $button = $input.parent().find("button");
        if ($input.val() === "") {
            $button.addClass("btn-default").removeClass("btn-primary");
        } else {
            $button.removeClass("btn-default").addClass("btn-primary");
        }
    },
    search: function (needle) {
        var self = this;
        this.fetch_existing(needle).then(function () {
            self.selected_existing();
        });
    },
    set_image: function (attachment, error) {
        var self = this;
        this.push(attachment);
        this.$('input.url').val('');
        this.fetch_existing().then(function () {
            self.selected_existing();
        });
    },
    form_submit: function (event) {
        var self = this;
        var $form = this.$('form[action="/web_editor/attachment/add"]');
        if (!$form.find('input[name="upload"]').val().length) {
            var url = $form.find('input[name="url"]').val();
            if (this.selected_existing().size()) {
                event.preventDefault();
                return false;
            }
        }
        $form.find('.well > div').hide().last().after('<span class="fa fa-spin fa-3x fa-refresh"/>');

        var callback = _.uniqueId('func_');
        this.$('input[name=func]').val(callback);
        window[callback] = function (attachments, error) {
            delete window[callback];
            _.each(attachments, function (record) {
                record.src = record.url || '/web/image/' + record.id;
                record.is_document = !(/gif|jpe|jpg|png/.test(record.mimetype));
            });
            if (error || !attachments.length) {
                self.file_selected(null, error || !attachments.length);
            }
            self.images = attachments;
            for (var i=0; i<attachments.length; i++) {
                self.file_selected(attachments[i], error);
            }
        };
    },
    file_selection: function () {
        this.$el.addClass('nosave');
        this.$('form').removeClass('has-error').find('.help-block').empty();
        this.$('button.filepicker').removeClass('btn-danger btn-success');
        this.$('form').submit();
    },
    file_selected: function(attachment, error) {
        var $button = this.$('button.filepicker');
        if (!error) {
            $button.addClass('btn-success');
            this.set_image(attachment);
        } else {
            this.$('form').addClass('has-error')
                .find('.help-block').text(error);
            $button.addClass('btn-danger');
        }

        if (!this.options.select_images) {
            // auto save and close popup
            this.parent.save();
        }
    },
    fetch_existing: function (needle) {
        var domain = [['res_model', '=', 'ir.ui.view']].concat(this.domain);
        if (needle && needle.length) {
            domain.push('|', ['datas_fname', 'ilike', needle], ['name', 'ilike', needle]);
        }
        return ajax.jsonRpc('/web/dataset/call_kw', 'call', {
            model: 'ir.attachment',
            method: 'search_read',
            args: [],
        }).then(this.proxy('fetched_existing'));
    },
    fetched_existing: function (records) {
        this.records = records;
        _.each(records, function (record) {
            record.src = record.url || '/web/image/' + record.id;
            record.is_document = !(/gif|jpe|jpg|png/.test(record.mimetype));
        });
        this.display_attachments();
    },
    display_attachments: function () {
        var self = this;
        var per_screen = IMAGES_PER_ROW * IMAGES_ROWS;
        var from = this.page * per_screen;
        var records = this.records;

        // Create rows of 3 records
        var rows = _(records).chain()
            .slice(from, from + per_screen)
            .groupBy(function (_, index) { return Math.floor(index / IMAGES_PER_ROW); })
            .values()
            .value();

        this.$('.help-block').empty();

        this.$('.existing-attachments').replaceWith(
            qweb.render(
                'web_editor.dialog.image.existing.content', {rows: rows}));
        this.parent.$('.pager')
            .find('li.next').toggleClass('disabled', (from + per_screen >= records.length));

        this.$el.find('.o_image').each(function () {
            var $div = $(this);
            if (/gif|jpe|jpg|png/.test($div.data('mimetype'))) {
                var $img = $('<img/>').addClass('img img-responsive').attr('src', $div.data('url') || $div.data('src'));
                $div.addClass('o_webimage').append($img);
            }
        });
        this.selected_existing();
    },
    select_existing: function (e) {
        var $img = $(e.currentTarget);
        var attachment = _.find(this.records, function (record) { return record.id === $img.data('id'); });
        this.selected_existing(attachment);
    },
    selected_existing: function () {
        var self = this;
        this.$('.existing-attachment-cell.media_selected').removeClass("media_selected");
        var $select = this.$('.existing-attachment-cell [data-src]').filter(function () {
            var $img = $(this);
        });
        $select.closest('.existing-attachment-cell').addClass("media_selected");
        return $select;
    },
    try_remove: function (e) {
        var $help_block = this.$('.help-block').empty();
        var self = this;
        var $a = $(e.target);
        var id = parseInt($a.data('id'), 10);
        var attachment = _.findWhere(this.records, {id: id});
        var $both = $a.parent().children();

        $both.css({borderWidth: "5px", borderColor: "#f00"});

        return ajax.jsonRpc('/web_editor/attachment/remove', 'call', {'ids': [id]}).then(function (prevented) {
            if (_.isEmpty(prevented)) {
                self.records = _.without(self.records, attachment);
                self.display_attachments();
                return;
            }
            $both.css({borderWidth: "", borderColor: ""});
            $help_block.replaceWith(qweb.render(
                'web_editor.dialog.image.existing.error', {
                    views: prevented[id]
                }
            ));
        });
    },
});


snippet.Class.include({

    // offer limited subset of snippets to MM
    compute_snippet_templates: function (html) {
        var self = this;
        var $html = $(html);
        var $left_bar = this.$el.find("#o_left_bar");
        var $ul = $html.siblings("ul");
        var $scroll = $html.siblings("#o_scroll");

        if (!$scroll.length) {
            throw new Error("Wrong snippets xml definition");
        }

        $ul.children().tooltip({
                delay: { "show": 500, "hide": 100 },
                container: 'body',
                title: function () {
                    return (navigator.appVersion.indexOf('Mac') > -1 ? 'CMD' : 'CTRL')+'+SHIFT+'+($(this).index()+1);
                },
                trigger: 'hover',
                placement: 'top'
            }).on('click', function () {$(this).tooltip('hide');});

        // t-snippet
        $html.find('[data-oe-type="snippet"][data-oe-name]').each(function () {
            var $div = $('<div/>').insertAfter(this).append(this).attr('name', $(this).data('oe-name'));
        });
        // end

        self.templateOptions = [];
        var selector = [];
        var $styles = $html.find("[data-js], [data-selector]");
        $styles.each(function () {
            var $style = $(this);
            var no_check = $style.data('no-check');
            var option_id = $style.data('js');
            var option = {
                'option' : option_id,
                'base_selector': $style.data('selector'),
                'selector': self._add_check_selector($style.data('selector'), no_check),
                '$el': $style,
                'drop-near': $style.data('drop-near') && self._add_check_selector($style.data('drop-near'), no_check, true),
                'drop-in': $style.data('drop-in') && self._add_check_selector($style.data('drop-in'), no_check),
                'data': $style.data()
            };
            self.templateOptions.push(option);
            selector.push(option.selector);
        });

        $styles.addClass("hidden");
        snippet.globalSelector.closest = function ($from) {
                var $temp;
                var $target;
                var len = selector.length;
                for (var i = 0; i<len; i++) {
                    $temp = selector[i].closest($from, $target && $target[0]);
                    if (!$target || $temp.length) {
                        $target = $temp;
                    }
                }
                return $target;
        };
        snippet.globalSelector.all = function ($from) {
                var $target;
                var len = selector.length;
                for (var i = 0; i<len; i++) {
                    if (!$target) $target = selector[i].all($from);
                    else $target = $target.add(selector[i].all($from));
                }
                return $target;
        };
        snippet.globalSelector.is = function ($from) {
                var len = selector.length;
                for (var i = 0; i<len; i++) {
                    if (selector[i].is($from)) {
                        return true;
                    }
                }
                return false;
        };

        var number = 0;

        // oe_snippet_body
        self.$snippets = $scroll.find(".o_panel_body").children()
            .addClass("oe_snippet")
            .each(function () {
                if (!$('.oe_snippet_thumbnail', this).size()) {
                    var $div = $(
                        '<div class="oe_snippet_thumbnail">'+
                        '</div>');
                    $div.find('span').text($(this).attr("name"));
                    $(this).prepend($div);

                    // from t-snippet
                    var thumbnail = $("[data-oe-thumbnail]", this).data("oe-thumbnail");
                    if (thumbnail) {
                        $div.find('.oe_snippet_thumbnail_img').css('background-image', 'url(' + thumbnail + ')');
                    }
                    // end
                }
                if (!$(this).data("selector")) {
                    $("> *:not(.oe_snippet_thumbnail)", this).addClass('oe_snippet_body');
                }
                number++;
            });

        Users.call('has_group', ['base.group_website_designer']).done(function(is_designer) {
            if (!is_designer) { 
                var hide_snippets = [self.$snippets[0], self.$snippets[1]];
                $(hide_snippets).css("display","none");
            }
        });
                      
        // hide scroll if no snippets defined
        if (!number) {
            this.$snippet.detach();
        } else {
            this.$el.find("#o_left_bar").removeClass("hidden");
        }
        $("body").toggleClass("editor_has_snippets", !!number);

        // select all default text to edit (if snippet default text)
        self.$snippets.find('.oe_snippet_body, .oe_snippet_body *')
            .contents()
            .filter(function() {
                return this.nodeType === 3 && this.textContent.match(/\S/);
            }).parent().addClass("o_default_snippet_text");
        $(document).on("mouseup", ".o_default_snippet_text", function (event) {
            $(event.target).selectContent();
        });
        $(document).on("keyup", function (event) {
            var r = $.summernote.core.range.create();
            $(r && r.sc).closest(".o_default_snippet_text").removeClass("o_default_snippet_text");
        });
        // end

        // clean t-oe
        $html.find('[data-oe-model], [data-oe-type]').each(function () {
            for (var k=0; k<this.attributes.length; k++) {
                if (this.attributes[k].name.indexOf('data-oe-') === 0) {
                    $(this).removeAttr(this.attributes[k].name);
                    k--;
                }
            }
        });
        // end

        $html.find('.o_not_editable').attr("contentEditable", false);

        $left_bar.html($html);

        // animate for list of snippet blocks
        $left_bar.on('click', '.scroll-link', function (event) {
            event.preventDefault();
            var targetOffset =  $($(this).attr("href")).position().top - $ul.outerHeight() + $scroll[0].scrollTop;
            $scroll.animate({'scrollTop': targetOffset}, 750);
        });
        $scroll.on('scroll', function () {
            var middle = $scroll.height()/4;
            var $li = $ul.find("a").parent().removeClass('active');
            var last;
            for (var k=0; k<$li.length; k++) {
                var li = $($li[k]);
                if (!li.data('target')) {
                    li.data('target', $($("a", li).attr("href")));
                }
                if (li.data('target').position().top > middle) {
                    break;
                }
                last = $li[k];
            }
            $(last).addClass("active");
        });
        // end

        // display scrollbar
        $(window).on('resize', function () {
            $scroll.css("overflow", "");
            var height = $left_bar.height() - $ul.outerHeight();
            $scroll.css("height", height);
            var $last = $scroll.children(":visible").last().children(".o_panel_body");
            $last.css({'min-height': (height-$last.prev().outerHeight())+'px'});
            if ($scroll[0].scrollHeight + $ul[0].scrollHeight > document.body.clientHeight) {
                $scroll.css("overflow", "auto").css("width", "226px");
            } else {
                $scroll.css("width", "");
            }
        }).trigger('resize');
        // end

        self.make_snippet_draggable(self.$snippets);
    },

    //prevent resize functionality for MM
    activate_overlay_zones: function($targets){
        var self = this;

        function is_visible($el){
            return     $el.css('display')    != 'none'
                    && $el.css('opacity')    != '0'
                    && $el.css('visibility') != 'hidden';
        }

        // filter out invisible elements
        $targets = $targets.filter(function(){ return is_visible($(this)); });

        // filter out elements with invisible parents
        $targets = $targets.filter(function(){
            var parents = $(this).parents().filter(function(){ return !is_visible($(this)); });
            return parents.length === 0;
        });

        $targets.each(function () {
            var $target = $(this);
            if (!$target.data('overlay')) {
                var $zone = $(qweb.render('web_editor.snippet_overlay'));
                // fix for pointer-events: none with ie9
                if (document.body && document.body.addEventListener) {
                    $zone.on("click mousedown mousedown", function passThrough(event) {
                        event.preventDefault();
                        $target.each(function() {
                           // check if clicked point (taken from event) is inside element
                            event.srcElement = this;
                            $(this).trigger(event.type);
                        });
                        return false;
                    });
                }

                $zone.appendTo('#oe_manipulators');
                Users.call('has_group', ['base.group_website_designer']).done(function(is_designer) {
                    if (!is_designer) { 
                        $("#oe_manipulators").find('.oe_handles').remove();
                    }
                });
                $zone.data('target',$target);
                $target.data('overlay',$zone);

                var timer;
                $target.closest('.o_editable').on("content_changed", function (event) {
                    clearTimeout(timer);
                    timer = setTimeout(function () {
                        if ($target.data('overlay') && $target.data('overlay').hasClass("oe_active")) {
                            self.cover_target($target.data('overlay'), $target);
                        }
                    },50);
                 });

                $('body').on("resize", resize);
            }
            self.cover_target($target.data('overlay'), $target);
        });
        return $targets;
    },

});
});