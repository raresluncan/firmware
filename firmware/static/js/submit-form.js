var base64Image;
form_data = {};

function submitForm(selector, successHandler, errorsHandler) {
  var form = document.getElementsByClassName(selector)[0];
  form.addEventListener('submit', function(ev) {
    ev.preventDefault();

    textareas = form.getElementsByTagName('textarea');
    for (var i=0; i<textareas.length; i++) {
      form_data[textareas[i].name] = textareas[i].value;
    }
    inputs = form.getElementsByTagName('input');
    for (i=0; i<inputs.length; i++) {
      form_data[inputs[i].name] = inputs[i].value;
    }
    selects = form.getElementsByTagName('select');
    for (i=0; i<selects.length; i++) {
      form_data[selects[i].name] = selects[i].value;
    }

    if(document.getElementById('picture') !== null)
    {
      form_data.picture = base64Image;
    }

    var request = new XMLHttpRequest();
    request.onreadystatechange = function() {
      if(request.readyState == 4 && request.status == 200) {
        console.log("READY4 STATUS 200 - POSTED");
        response = JSON.parse(request.response);
        if(response.success == true)
        {
          successHandler(response.data, response.user);
        }
        if(response.success == false)
        {
          errorsHandler(response.errors);
        }
      }
    };
    request.open("POST", form.action, true);
    request.setRequestHeader("Content-type", "application/json");
    request.send(JSON.stringify(form_data));
  });
}


if(document.getElementById("picture")) {
  document.getElementById("picture").addEventListener("change", function() {
    var info =  image_to_viewport("viewport", document.getElementById('picture'), function(base64Img) {
      base64Image = base64Img;
    });
  }, true);
}
