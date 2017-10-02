function addReview(response_data, user_data) {

  var review_list = document.getElementById("review-list");
  var list_item = document.createElement('li');
  list_item.setAttribute("class", "details-reviews");

  var username_and_avatar = document.createElement('div');
  username_and_avatar.setAttribute("class", "username-avatar");

  var username = document.createElement('h2');
  username.setAttribute("class", "details-user");
  username.innerHTML = user_data.username;

  var avatar = document.createElement("img");
  avatar.setAttribute("class", "review-avatar");
  if(user_data.avatar !== "default.jpg") {
    avatar.setAttribute("src", "../static/Avatars/"+user_data.avatar);
  }
  else {
    avatar.setAttribute("src", "../static/Defaults/user/"+user_data.avatar);
  }

  var review_message = document.createElement("p");
  review_message.setAttribute("class", "details-user-review");
  review_message.innerHTML = response_data.message;

  review_list.insertBefore(list_item, review_list.firstChild);
  list_item.appendChild(username_and_avatar);
  list_item.appendChild(review_message);
  username_and_avatar.appendChild(username);
  username_and_avatar.appendChild(avatar);

  review_list.scrollTop = 0;
  document.getElementById("title-reviews").scrollIntoView();
  document.getElementById('message').value = "";

  flashMessage("Review added sucessfully");
}

submitForm("reviews-bottom", addReview, flash_errors);
