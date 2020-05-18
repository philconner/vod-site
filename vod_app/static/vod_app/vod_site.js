//;function showEmbedForm() {
//    var target_div = document.getElementById("embed-form");
//    var required_inputs = $("#embed-form .embed-form-required");
//    var nonrequired_inputs = $("#upload-form .upload-form-required");
//    var other_div = document.getElementById("upload-form");
//    var picture_div = document.getElementById("picture-forms");
//
//    if (target_div.style.display === "none") {
//        // show
//        target_div.style.display = "block";
//        var i;
//        for (i of required_inputs) {
//            var child;
//            for (child of i.children) {
//                child.required = true;
//            }
//        }
//        for (i of nonrequired_inputs) {
//            var child;
//            for (child of i.children) {
//                child.required = false;
//            }
//        }
//        picture_div.style.display = "block";
//        other_div.style.display = "none";
//    } else {
//        // hide
//        target_div.style.display = "none";
//        var i;
//        for (i of required_inputs) {
//            var child;
//            for (child of i.children) {
//                child.required = false;
//            }
//        }
//        picture_div.style.display = "none";
//    }
//}
//
//function showUploadForm() {
//    var target_div = document.getElementById("upload-form");
//    var required_inputs = $("#upload-form .upload-form-required");
//    var nonrequired_inputs = $("#embed-form .embed-form-required");
//    var other_div = document.getElementById("embed-form");
//    var picture_div = document.getElementById("picture-forms");
//
//    if (target_div.style.display === "none") {
//        // show
//        target_div.style.display = "block";
//        var i;
//        for (i of required_inputs) {
//            var child;
//            for (child of i.children) {
//                child.required = true;
//            }
//        }
//        for (i of nonrequired_inputs) {
//            var child;
//            for (child of i.children) {
//                child.required = false;
//            }
//        }
//        picture_div.style.display = "block";
//        other_div.style.display = "none";
//    } else {
//        // hide
//        target_div.style.display = "none";
//        var i;
//        for (i of required_inputs) {
//            var child;
//            for (child of i.children) {
//                child.required = false;
//            }
//        }
//        picture_div.style.display = "none";
//    }
//}

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();
});

 function updateElementIndex(el, prefix, ndx) {
        var id_regex = new RegExp('(' + prefix + '-\\d+)');
        var replacement = prefix + '-' + ndx;

        if ($(el).attr("for")) {
            $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
        }

        if (el.id) {
            el.id = el.id.replace(id_regex, replacement);
        }

        if (el.name) {
            el.name = el.name.replace(id_regex, replacement);
        }
    }

    function cloneMore(selector, prefix) {
        var newElement = $(selector).clone(true);
        var total = $('#id_' + prefix + '-TOTAL_FORMS').val();

        newElement.find(':input:not([type=button]):not([type=submit]):not([type=reset])').each(function() {
            var name = $(this).attr('name').replace('-' + (total-1) + '-', '-' + total + '-');
            var id = 'id_' + name;
            $(this).attr({'name': name, 'id': id}).val('').removeAttr('checked');
        });

        newElement.find('label').each(function() {
            var forValue = $(this).attr('for');
            if (forValue) {
              forValue = forValue.replace('-' + (total-1) + '-', '-' + total + '-');
              $(this).attr({'for': forValue});
            }
        });

        total++;
        $('#id_' + prefix + '-TOTAL_FORMS').val(total);
        $(selector).after(newElement);
        var conditionRow = $('.form-row:not(:last)');

//        conditionRow.find('.btn.add-form-row').remove();
//        .removeClass('add-form-row').addClass('remove-form-row')
//        .html('<span class="glyphicon glyphicon-minus" aria-hidden="true">-</span>');
        return false;
    }

    function deleteForm(prefix, btn) {
        var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
        if (total > 1){
            btn.closest('.form-row').remove();
            var forms = $('.form-row');
            $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
            for (var i=0, formCount=forms.length; i<formCount; i++) {
                $(forms.get(i)).find(':input').each(function() {
                    updateElementIndex(this, prefix, i);
                });
            }
        }
        return false;
    }

    $(document).on('click', '.add-form-row', function(e) {
        e.preventDefault();
        cloneMore('.form-row:last', 'form');
        return false;
    });

    $(document).on('click', '.remove-form-row', function(e) {
        e.preventDefault();
        deleteForm('form', $(this));
        return false;
    });