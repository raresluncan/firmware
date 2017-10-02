function flashMessage(message) {

  var alerts = document.getElementById("alerts");
  if (alerts == null) {
    alerts = document.createElement('div');
    alerts.setAttribute("class", "alerts");
    alerts.setAttribute("id", "alerts");
  }
  document.getElementsByClassName('header')[0].appendChild(alerts);
  var alert_body = document.createElement('div');
  alert_body.setAttribute("class", "alert-flash");
  alert_body.innerHTML = message;


  var alert_close = document.createElement('span');
  alert_close.setAttribute("class", "closebtn");
  alert_close.setAttribute("onclick", "this.parentElement.style.display='none';");
  alert_close.innerHTML="&times;";

  alert_body.appendChild(alert_close);
  alerts.appendChild(alert_body);

  setTimeout(function() {
    fade_out(alert_body);
  }, 2700);
}
