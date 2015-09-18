/*jslint white: true, onevar: true, undef: true, newcap: true, nomen: true,
  plusplus: true, bitwise: true, regexp: false, indent: 4 */

/*globals jQuery, form_modified_message, ajax_noresponse_message */

/* global message strings are from jsvariables.py in CMFPlone */

if(require === undefined){
  // plone 4
  require = function(reqs, torun){
    'use strict';
    return torun(window.jQuery);
  };
}

if (window.jQuery && define) {
  define( 'jquery', [], function () {
    'use strict';
    return window.jQuery;
  } );
}


require([
  'jquery',
  'ace'
], function($) {
  'use strict';

var init = function(){
    if (!window.ace){
        // XXX hack...
        // wait, try loading later
        setTimeout(function() {
          init();
        }, 200);
        return;
    }

    var editor = ace.edit("modelEditor"),
        session = editor.getSession(),
        myform = $("#saveform"),
        doc_changed = false;

    // editor tuneup
    editor.setTheme("ace/theme/monokai");
    session.setMode("ace/mode/xml");
    session.setTabSize(4);
    session.setUseSoftTabs(true);
    session.setUseWrapMode(true);
    editor.setHighlightActiveLine(false);
    // Make save keystroke trigger save-form submit
    editor.commands.addCommand({
        name: "save",
        bindKey: {win: "Ctrl-S", mac: "Command-S"},
        exec: function() {
            myform.submit();
        }
    });

    // enable save submit button on change
    session.on('change', function(e) {
        $('#saveform :submit').removeAttr('disabled');
        doc_changed = true;
    });

    // unload protection
    // See http://dev.w3.org/html5/spec-LC/history.html#unloading-documents
    $(window).on("beforeunload", function(event) {
        if (doc_changed) {
            return form_modified_message;
        } else {
            event.returnValue = "";
        }
    });

    // form submit handler; ajax posts data
    myform.on("submit", function(event) {
        var action = myform.attr('action');

        // prevent real submit
        event.preventDefault();

        // stuff the editor contents into the form
        // for easy serialization
        $('#savesource').val(editor.getValue());

        $.post(action, myform.serialize(), function (rez) {
            if (rez.success) {
                var messagespan = $("#messagespan");

                doc_changed = false;
                // disable save button
                $('#saveform :submit')
                    .attr('disabled', 'disabled')
                    .removeClass('submitting');
                messagespan.html(rez.message);
                messagespan.show().fadeOut(1000);
            } else {
                alert(rez.message);
            }
        }, 'json')
        .fail(function() {
            alert(ajax_noresponse_message);
        });

    });

    function setEditorSize () {
      var wheight = $(window).height();
      $("#rules-editor").height(wheight);
      $("#modelEditor").height(wheight-80);
    }
    $(window).resize(function() {
      setEditorSize();
    });
    setEditorSize();
};

$().ready(function() {
    init();
});

});
