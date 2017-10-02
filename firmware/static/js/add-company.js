function addCompany(response_data, user_data) {
  form_locked = document.getElementsByClassName("add-company-layout")[0];
  form_locked.style.display = "none";
  if(response_data.flash == "add") {
    flashMessage("Please wait a moment while we add "+response_data.name+" to our list");
  }
  else {
    flashMessage("Please wait a moment while we update your company");
  }
  setTimeout(function() {
    window.location.replace("http://0.0.0.0:5000/details/"+response_data.id);
  }, 3700);
  form_locked.style.visibility = "flex";
}

document.getElementById('category_id').addEventListener("change", function() {
  var categories = document.getElementById('category_id');
  categories.options[categories.options.selectedIndex].selected = true;
});

submitForm("add-company", addCompany, flash_errors);
