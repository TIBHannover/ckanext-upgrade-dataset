function formatState (state) {
    if (!state.id) {
      return $.trim(state.text);
    }    
    let image_url = $('div[value="' + $.trim(state.text) + '"]').text(); 
    if(image_url == 'None'){
      let $state = $.trim(state.text) + '<br><br>';
      return $state;
    }   
    var $state = $(
      '<span>' + $.trim(state.text) + '<br><img src="' + $.trim(image_url) + '"' + 'class="responsive">' + '</span>'
    );
    return $state;
  };

$(document).ready(function(){
    $('.machine_dropdown').parent().parent().find('label').hide(); 
    $("select.machine_dropdown").select2({
        formatResult: formatState
      });
    $('.machine_dropdown').change(function(){
        let id = $(this).attr('id');
        id = id[id.length - 1];
        $('#machine_name_' + id).val($.trim($(this).select2('data').text));        
    });

});