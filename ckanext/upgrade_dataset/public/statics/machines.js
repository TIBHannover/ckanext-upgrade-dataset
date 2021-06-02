$(document).ready(function(){
    $('#not_find').change(function(){
        if($(this).is(':checked')){
            $('#manual_link_box').show();
            $('#machines_dropdown').prop('disabled', true);
        }
        else{
            $('#manual_link_box').hide();
            $('#machines_dropdown').prop('disabled', false);
        }
    });


});