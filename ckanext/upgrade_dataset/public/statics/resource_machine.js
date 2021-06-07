$(document).ready(function(){
    $.ajax({
        url: $('#get_link_url').val(),
        cache:false,        
        type: "GET",
        success: function(result){
            $('#machine_url_anchor').attr('href', result);
            $('#machine_url_anchor').text(result);

        }
    });



});

