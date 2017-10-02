function addUser(response_data, user_data) {
  flashMessage("New user, "+response_data.username+", added sucessfully");
  setTimeout(function() {
    window.location.replace("http://0.0.0.0:5000/home#reload-point");
  }, 1700);
}

submitForm("add-user", addUser, flash_errors);
