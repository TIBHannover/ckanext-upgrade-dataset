function formatState (state) {
    if (!state.id) {
      return $.trim(state.text);
    }    
    let image_url = $('div[value="' + $.trim(state.text) + '"]').text();
    // console.info('.machine_url_div[value="' + $.trim(state.text) + '"]');
    var $state = $(
      '<span>' + $.trim(state.text) + '<br><img src="' + $.trim(image_url) + '"' + 'class="responsive">' + '</span>'
    );
    return $state;
  };

$(document).ready(function(){
    $('.machine_dropdown').parent().parent().find('label').hide();     
    // $('select.machine_dropdown').select2();    
    $("select.machine_dropdown").select2({
        formatResult: formatState
      });
    $('.machine_dropdown').change(function(){
        let id = $(this).attr('id');
        id = id[id.length - 1];
        $('#machine_name_' + id).val($(this).find(":selected").text());
        // if($(this).find(":selected").val() != '0'){
        //     // let id = '#' + $(this).find(":selected").text().replace(/ /g, "_").replace(/\//g, "_");
        //     let image_url = $(this).find(":selected").val(); 
        //     let resource_id = $(this).attr('id').split('machines_dropdown_')[1];
        //     $('#image_div_' + resource_id).find('a').attr('href', image_url);
        //     $('#image_div_' + resource_id).fadeIn();            
        // }
        
    });
    

});