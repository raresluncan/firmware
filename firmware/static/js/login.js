function loginSuccess(response_data, user_data) {
  form_locked = document.getElementsByClassName("login-data")[0];
  button_locked = document.getElementById("log-button");
  button_locked.style.display = "none";
  form_locked.style.display = "none";
  flashMessage("Welcome back, dear "+response_data.username+".Glad to see you again!");
  setTimeout(function() {
    window.location.replace("http://0.0.0.0:5000/home#reload-point");
  }, 2000);
}

submitForm("login-data", loginSuccess, flash_errors);
