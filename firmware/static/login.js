function change_items() {
    var x = document.getElementById('-profile-pic');
    if (x.style.display === 'none') {
        x.style.display = 'block';
        var y = document.getElementById('-login-label').value
    } else {
        x.style.display = 'none';
    }
}
