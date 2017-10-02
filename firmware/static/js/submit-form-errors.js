var okToAlert = true;
function flash_errors(errors){
  if(okToAlert)
  {
  var alerts = document.getElementById("alerts");
    if (alerts == null) {
      alerts = document.createElement('div');
      alerts.setAttribute("class", "alerts");
      alerts.setAttribute("id", "alerts");
    }
    document.getElementsByClassName('header')[0].appendChild(alerts);
    for(var error in errors) {
      if(errors.hasOwnProperty(error)) {
        var alert_body = document.createElement('div');
        alert_body.setAttribute("class", "alert");
        alert_body.innerHTML = errors[error];

        var alert_close = document.createElement('span');
        alert_close.setAttribute("class", "closebtn");
        alert_close.setAttribute("onclick", "this.parentElement.style.display='none';");
        alert_close.innerHTML="&times;";

        alert_body.appendChild(alert_close);
        alerts.appendChild(alert_body);
      }
    }
    okToAlert = false;
    setTimeout(function(){
        fade_out(alerts);
        setTimeout(function(){ okToAlert=true; }, 300);
    }, 1500);
  }
}
