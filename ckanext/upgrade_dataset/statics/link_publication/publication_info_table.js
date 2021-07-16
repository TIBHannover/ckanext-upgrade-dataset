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

    $('#doi-form').submit(function(e){
        e.preventDefault();
        let doi_input = $('#doi').val();
        $.ajax({
            url: $('#doi-validity-url').val(),
            cache:false,   
            data: {'doi_url': doi_input},
            // dataType: 'json',      
            type: "POST",
            success: function(result){
                if(result != '1'){                               
                    return false;             
                }
                else{
                    // $('#loading_publications').hide();
                }                        
            }
        });
        
    });
    
});