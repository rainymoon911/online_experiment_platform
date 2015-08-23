function JennystartXBlock(runtime, element) {
  var editor;
  $(element).find('#save_btn').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'save_file');
    var data = {
      codeData: editor.getValue()
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      window.location.reload(false);
    });
  });
  
  $(element).find('#open_btn').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'open_file');
    var data = {
      relative_path: $("#relative_path", element).val()
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
    });
  });
  
  $(element).find('#commit_btn').bind('click', function() {
    var handlerUrl = runtime.handlerUrl(element, 'commit_to_git');
    var data = {
      commit_message: $("#commit_message", element).val()
    };
    $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
      alert("commit done");
    });
  });

  $(element).find('#clean_btn').bind('click', function() {
    editor.setValue("");
  });
    
  $(element).find('.fullscreen').bind('click', function() {
      var screen = document.getElementById("jennystart_block");
  
      if(screen.requestFullscreen){
            screen.requestFullscreen();
      }
      else if (screen.mozRequestFullScreen){
          screen.mozRequestFullScreen();
      }
      else if (screen.webkitRequestFullscreen){
          screen.webkitRequestFullscreen();
      }
  });
    


    $(function($){
        /* Here's where you'd do things on page load. */
        editor = CodeMirror.fromTextArea(document.getElementById("code"), {
            lineNumbers: true,
            styleActiveLine: true,
            matchBrackets: true,
            mode: "text/x-c++src",
            extraKeys: {
                "F11": function(cm) {
                    cm.setOption("fullScreen", !cm.getOption("fullScreen"));
                },
                "Esc": function(cm) {
                    if (cm.getOption("fullScreen")) cm.setOption("fullScreen", false);
                }
            }


        });


    });
}
