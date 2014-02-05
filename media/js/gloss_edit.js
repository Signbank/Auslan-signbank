/**
 * @author Steve Cassidy
 */
 $(document).ready(function() {
     configure_edit();
     //disable_edit();
     $('#enable_edit').click(toggle_edit);
     
     var tagApi = $("#taginput").tagsManager({
         tagsContainer: "#tagcontainer"
     });
     
     
     var tagEngine = new Bloodhound({
        datumTokenizer: function(d) { return Bloodhound.tokenizers.whitespace(d.name); },
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        name: 'tags',
        prefetch: {
            url : '/dictionary/ajax/tags',
            filter: function(list) {
                     return $.map(list, function(tag) { return { name: tag }; });
            }
        }
     });
     
     tagEngine.initialize();
     
     $("#taginput").typeahead(null, {displayKey: 'name', source: tagEngine.ttAdapter()}).on('typeahead:selected', function (e, d) {
 
      tagApi.tagsManager("pushTag", d.value);
 
    });
     
     
     
     /*
     $('#delete_video').confirm({
        msg:'Delete this video?',
        timeout:3000
     });
     */
    
    // setup requried for Ajax POST
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            } 
        }
    });

    ajaxifyTagForm();
     
 });

function disable_edit() {
    $('.edit').editable('disable');
    $('.edit').css('color', 'black');
    $('#edit_message').text(''); 
    $('.editform').hide();
};

function enable_edit() {
    $('.edit').editable('enable');
    $('.edit').css('color', 'red');
    $('#edit_message').text('Click on red text to edit  '); 
    $('.editform').show();   
};

function toggle_edit() {
    if ($('#enable_edit').hasClass('edit_enabled')) {
        disable_edit();
        $('#enable_edit').removeClass('edit_enabled');
        $('#enable_edit').text('Enable Edit');
    } else {
        enable_edit();
        $('#enable_edit').addClass('edit_enabled');
        $('#enable_edit').text('Disable Edit');
    }
}

function configure_edit() {
     $('.edit_text').editable(edit_post_url, {
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         indicator : 'Saving...',
         tooltip   : 'Click to edit...',
         placeholder : 'No Value Set',
         cancel    : 'Cancel',
         submit    : 'OK'
     });
     $('.edit_area').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'textarea',
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     });
     $('.edit_role').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'select',
         data      : definition_role_choices,
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     });
     $('.edit_language').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'multiselect',
         data      : languages,
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     });
     $('.edit_dialect').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'multiselect',
         data      : dialects,
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     });     
     $('.edit_check').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'checkbox',
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...',
         checkbox: { trueValue: 'Yes', falseValue: 'No' }
     });
     
     $('.edit_handshape').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'select',
         data      : handshape_choices,
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     });
     $('.edit_location').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'select',
         data      : location_choices,
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     });
     $('.edit_palm').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'select',
         data      : palm_orientation_choices,
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     });
     $('.edit_relori').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'select',
         data      : relative_orientation_choices,
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     }); 
     $('.edit_sec_location').editable(edit_post_url, { 
         submitdata  : {'csrfmiddlewaretoken': csrf_token},
         type      : 'select',
         data      : secondary_location_choices,
         cancel    : 'Cancel',
         submit    : 'OK',
         placeholder : 'No Value Set',
         tooltip   : 'Click to edit...'
     });                  
}


/* 
 * http://stackoverflow.com/questions/1597756/is-there-a-jquery-jeditable-multi-select-plugin
 */

$.editable.addInputType("multiselect", {
    element: function (settings, original) {
        var select = $('<select multiple="multiple" />');

        if (settings.width != 'none') { select.width(settings.width); }
        if (settings.size) { select.attr('size', settings.size); }

        $(this).append(select);
        return (select);
    },
    content: function (data, settings, original) {
        /* If it is string assume it is json. */
        if (String == data.constructor) {
            eval('var json = ' + data);
        } else {
            /* Otherwise assume it is a hash already. */
            var json = data;
        }
        for (var key in json) {
            if (!json.hasOwnProperty(key)) {
                continue;
            }
            if ('selected' == key) {
                continue;
            }
            var option = $('<option />').val(key).append(json[key]);
            $('select', this).append(option);
        }

        if ($(this).val() == json['selected'] ||
                            $(this).html() == $.trim(original.revert)) {
            $(this).attr('selected', 'selected');
        }

        /* Loop option again to set selected. IE needed this... */
        $('select', this).children().each(function () {
            if (json.selected) {
                var option = $(this);
                $.each(json.selected, function (index, value) {
                    if (option.val() == value) {
                        option.attr('selected', 'selected');
                    }
                });
            } else {
                if (original.revert.indexOf($(this).html()) != -1)
                    $(this).attr('selected', 'selected');
            }
        });
    }
});


     
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) { // >
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

    
function ajaxifyTagForm() {
    // ajax form submission for tag addition and deletion
    $('.tagdelete').click(function() {
        var action = $(this).attr('href');
        var tagid = $(this).attr('id');
        var tagelement = $(this).parents('.tagli');
        
        $.post(action, 
              {tag: tagid, 'delete': "True" }, 
               function(data) {
                    if (data == 'deleted') {
                        // remove the tag from the page 
                       tagelement.remove();
                    }
               });
        
        return false;
    });
    
    $('#tagaddform').submit(function(){
        $.post($(this).attr('action'), $(this).serialize(),
                function(data) {
                   // response is a new tag list
                   $('#tags').replaceWith(data);
                   ajaxifyTagForm();
               });
        return false;
    });
}
    
    
     


      
      