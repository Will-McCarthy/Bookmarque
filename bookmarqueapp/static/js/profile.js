var passwordformat = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;
var passwordHidden = true;

var $ = function(id) {
  return document.getElementById(id);
} //$

function changeCard() {
    let option = $('card-selector').value;
    let cardDisplays = document.getElementsByClassName('card-information');
    for (let i = 0; i < cardDisplays.length; i++) {
      cardDisplays[i].style.display = 'none';
    }
    $(option).style.display = 'block';
  } //changeCard

/*
 * Toggle whether password is hidden behind dots.
 */
function togglePassword() {

  let password = $('password-visible');
  let placeholder = $('password-hidden');
  let toggle = $('toggle-password');


  if (password.style.display == "none") {
    placeholder.style.display = "none";
    password.style.display = "inline";
    toggle.innerHTML = "Hide Password";
  } else {
    password.style.display = "none";
    placeholder.style.display = "inline";
    toggle.innerHTML = "Display Password";
  }


}
