$(document).ready(function(){        
    let url = $('#package_name').attr('dest');
    $.ajax({
        url: url,
        cache:false,   
        // dataType: 'json',      
        type: "GET",
        success: function(result){
            if(result != '0'){                               
                $('#material_info_header_tr').after(result);
                $('#publication_section').show();                
            }                        
        }
    });
    
});