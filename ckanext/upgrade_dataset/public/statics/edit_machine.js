$(document).ready(function(){
    $('.machine_dropdown').parent().parent().find('label').hide(); 
    $('.machine_dropdown').select2();
    $('.machine_dropdown').change(function(){
        let id = $(this).attr('id');
        id = id[id.length - 1];
        $('#machine_name_' + id).val($(this).find(":selected").text());
        if($(this).find(":selected").val() != '0'){
            let id = '#' + $(this).find(":selected").text().replace(/ /g, "_").replace(/\//g, "_");
            let image_url = $(id).text();
            console.info(id);                                 
            $('#machine-preview').attr('src', image_url);
            $('#machine_image_modal').modal('show');
        }
    });
    

});