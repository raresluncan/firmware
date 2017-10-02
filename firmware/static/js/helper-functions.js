function fade_out(element) {
  var op = 1;
  var timer = setInterval(function () {
      if (op <= 0.05) {
        clearInterval(timer);
        element.style.display = 'none';
        element.parentNode.removeChild(element);
      }
      element.style.opacity = op;
      element.style.filter = 'alpha(opacity=' + op * 100 + ")";
      op -= op * 0.05;
  }, 5);
}


function image_to_viewport(vieportId, input, callback) {
    var canvas = document.getElementById(vieportId);
    context = canvas.getContext('2d');
    if(input.files && input.files[0]) {
      var fr = new FileReader();
      fr.onload = function(e) {
         var img = new Image();
         img.addEventListener("load", function() {
           canvas.width = img.width;
           canvas.height = img.height;
           context.drawImage(img, 0, 0);
           base64image = getBase64Image(canvas);
           callback(base64image);
         });
         img.src = e.target.result;
      };
      fr.readAsDataURL( input.files[0] );
  }
}


function getBase64Image(canvas) {
  if(canvas)
  {
    dataURL = canvas.toDataURL('image/jpeg');
    return dataURL;
  }
  return "NO CANVAS ERROR";
}


if(document.getElementById('category_id') != null) {
  document.getElementById('category_id').addEventListener("change", function(){
    var categories = document.getElementById('category_id');
    categories.options[categories.options.selectedIndex].selected = true;
    console.log("done somethign");
  });
}
