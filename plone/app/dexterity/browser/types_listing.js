(function($){
$(document).ready(function() {

    common_content_filter = '#content>*:not(div.configlet),dl.portalMessage.error,dl.portalMessage.info';

    $('.action').css('display', 'inline');

    // add new type form
    $('#add-type').prepOverlay({
        subtype: 'ajax',
        filter: '#content',
        formselector: '#add-type-form',
        noform: function(el) {
            var o = $(el), emsg = o.find('dl.portalMessage.error');
            if (emsg.length) {
                o.children().replaceWith(emsg);
                return false;
            } else {
                return 'redirect';
            }
        },
        redirect: function (el, responseText) {
            var mo = responseText.match(/<a href="(\S+?)\/@@fields"/i);
            if (mo.length === 2) {
                return mo[1] + '/@@fields';
            }
            return location;
        }
    });

    // clone type form
    $('#crud-edit-form-buttons-clone').click(function(e) {
      var selected = $('input[id$=-widgets-select-0]:checked');
      if (selected.length == 1) {
          e.preventDefault();
          $(this).removeClass('submitting');
          var type_link = $('a', selected.closest('tr'));
          var el = $('<' + 'a href="' + type_link.attr('href') + '/@@clone"><' + '/a>').appendTo('body');
          el.prepOverlay({
              subtype: 'ajax',
              filter: common_content_filter,
              formselector: '#clone-type-form',
              noform: 'reload'
          })
          el.click();
      }
    });

    // delete type confirmation
    $('#crud-edit-form-buttons-delete').click(function(e) {
        var items = 0;
        $('td.count').closest('tr').has('input:checked').each(function() {
          items += parseInt($('td.count .int-field', this).html().trim());
        });
        if (items) {
          var msg = 'WARNING: There are existing instances of these content types which will break.\n\nAre you sure you want to delete these types?';
        } else {
          var msg = 'Are you sure you want to delete these types?';
        }
        if(!confirm(msg)) {
            $(this).removeClass('submitting');
            e.preventDefault();
        }
    });

    // set id from title
    $('#form-widgets-title').live('change', function () {
        var id = $.plone_schemaeditor_normalize_string($(this).val());
        $('#form-widgets-id').val(id);
    });
});
})(jQuery);
