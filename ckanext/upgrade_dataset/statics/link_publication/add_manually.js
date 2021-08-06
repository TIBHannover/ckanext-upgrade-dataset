$(document).ready(function(){
    $("#pub-type").select2();
    $('#years-select').select2();
    $('select.month-select').select2();

    $('#pub-type').change(function(){
        let pubType = $(this).select2('data').text;
        if (pubType == 'article'){
            $('.pub-type-section').hide();
            $('#article-section').fadeIn();
        }
        else if (pubType == 'techreport'){
            $('.pub-type-section').hide();
            $('#section-tech-report').fadeIn();
        }
        else if (['conference', 'inproceedings', 'proceedings'].includes(pubType)){
            $('.pub-type-section').hide();
            $('#conference-section').fadeIn();
        }
        else if (pubType == 'inbook'){
            $('.pub-type-section').hide();
            $('#inbook-section').fadeIn();
        }
        else if (pubType == 'incollection'){
            $('.pub-type-section').hide();
            $('#incollecion-section').fadeIn();
        }
        else if (pubType == 'book'){
            $('.pub-type-section').hide();
            $('#book-section').fadeIn();
        }
        else if (['masterthesis', 'phdthesis'].includes(pubType)){
            $('.pub-type-section').hide();
            $('#thesis-section').fadeIn();
        }
        else{
            $('.pub-type-section').hide();            
        }

    });

    $('#save-btn').click(function(){        
        form_validator();
        
    });



});

function form_validator(){
    let result = true;
    $('.pub-type-select').css('border', '');
    $('#pub-title').css('border', '');
    $('#authors').css('border', '');
    if ($('#pub-type').select2('data') == null){        
        $('.pub-type-select').css('border', '2px solid red');
        result = false;
    }
    if ($('#pub-title').val() == ''){        
        $('#pub-title').css('border', '2px solid red');
        result = false;
    }
    if ($('#authors').val() == ''){        
        $('#authors').css('border', '2px solid red');
        result = false;
    }
    if(!result){
        $('#mandatory-text').css('color', 'red');
    }

    return result;
}