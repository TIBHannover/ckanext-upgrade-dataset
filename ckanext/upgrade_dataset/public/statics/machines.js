$(document).ready(function(){
    $('.machine_dropdown').parent().parent().find('label').hide(); 
    
    $('.notFindCheckBox').change(function(){
        let id = $(this).attr('id');
        id = id[id.length - 1];
        if($(this).is(':checked')){
            $('#manual_link_box' + id).fadeIn();
            $('#machines_dropdown' + id).fadeOut();
        }
        else{
            $('#manual_link_box' + id).fadeOut();
            $('#machines_dropdown' + id).fadeIn();
        }
    });



});