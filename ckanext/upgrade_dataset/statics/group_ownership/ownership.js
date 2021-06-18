$(document).ready(function(){
    $('.org_dropdown').select2();
    $('.group_dropdown').select2();
    $('#ownership-form').submit(function(e){
        $('#org_group_error').hide();
        $('.group_dropdown').css('border', '');
        $('.org_dropdown').css('border', '');
        let org = $('#org_dropdown').find(':selected').val();
        let group = $('#groups_dropdown').find(':selected').val();
        if(org == '0'){
            e.preventDefault();
            $('#org_group_error').show();
            $('.org_dropdown').css('border', '2px solid red');
        } 
        if(group == '0'){
            e.preventDefault();
            $('#org_group_error').show();
            $('.group_dropdown').css('border', '2px solid red');
        }          
    });
});