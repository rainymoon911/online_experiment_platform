function CodeBrowserBlock(runtime, element) {
  $(element).find('#generate_btn').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'generate');
    var data = {
      lab: $("#lab", element).val()
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      window.location.reload(true);
    });
  });
  $(element).find('#generate_local_btn').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'generate_local');
    var data = {
      lab: $("#lab", element).val()
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      window.location.reload(true);
    });
  });

  $(element).find('#edit_btn').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'edit');
    
    var data = {
      src: parent.document.getElementById("codeview").contentWindow.location.href
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      if (response.result == true) {
      window.location.href = "http://166.111.68.45:11133/courses/BIT/CS101/2014T1/courseware/0b64b532c9f44b2c9c23a87a2b1f8104/da4d2d1648bf49baa59c08715acfcd38/";
     } else {
            $('.error-message', element).html('Error: ' + response.message);
     }
     
    });
  });
}
