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
        let form_validity = form_validator();
        if(form_validity){
            send_data();
        }        
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


function send_data(){
    var formdata = new FormData();
    let pubType = $('#pub-type').select2('data').text;
    formdata.set('type', pubType);
    formdata.set('title', $('#pub-title').val()); 
    formdata.set('author', $('#authors').val());
    formdata.set('year', $('#years-select').select2('data').text);
    formdata.set('publisher', $('#publisher').val());
   
    if (pubType == 'article'){
        formdata.set('journal', $('#article-journal').val());
        formdata.set('volume', $('#article-volume').val());
        formdata.set('page', $('#article-pages').val());
        formdata.set('month', $('#article-month').select2('data').text);
        send_request(formdata);

    }
    else if (pubType == 'techreport'){
        let reportNumber = $('#report-number').val();
        let institution = $('#report-ins').val();
        let month = $('#report-month').select2('data').text;
        let address = $('#report-address').val();

    }
    else if (['conference', 'inproceedings', 'proceedings'].includes(pubType)){
        let bookTitle = $('#conf-booktitle').val();
        let series = $('#conf-series').val();
        let address = $('#conf-address').val();
        let pages = $('#conf-pages').val();

    }
    else if (pubType == 'inbook'){
        let address = $('#inbook-address').val();
        let pages = $('#inbook-pages').val();

    }
    else if (pubType == 'incollection'){
        let editors = $('#incollecion-editor').val();
        let address = $('#incollecion-address').val();
        let pages = $('#incollecion-pages').val();
        let bookTitle = $('#incollecion-booktitle').val();

    }
    else if (pubType == 'book'){
        let address = $('#book-address').val();

    }
    else if (['masterthesis', 'phdthesis'].includes(pubType)){
        let address = $('#thesis-address').val();
        let month = $('#thesis-month').select2('data').text;
        let school = $('#thesis-school').val();

    }
    else{
        // other types
    }
}

function send_request(data){
    let dest_url = '';
    let req = new XMLHttpRequest();
    req.open("POST", dest_url);
    req.send(data);
}