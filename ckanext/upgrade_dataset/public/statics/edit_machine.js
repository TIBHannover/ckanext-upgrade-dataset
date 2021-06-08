$(document).ready(function(){
    $('.machine_dropdown').parent().parent().find('label').hide(); 
    $('.machine_dropdown').change(function(){
        let id = $(this).attr('id');
        id = id[id.length - 1];
        $('#machine_name_' + id).val($(this).find(":selected").text());
    });
    

});