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
                $('#loading_publications').hide();
                $('#publication_section').show();                
            }
            else{
                $('#loading_publications').hide();
            }                        
        }
    });

    // $('#doi-form').submit(function(){
    //     let doi_input = $('#doi').val();

        
        
        
        
    //     return false;
    // });
    
});