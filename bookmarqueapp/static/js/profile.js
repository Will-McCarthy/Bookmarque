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
// function togglePassword() {
//   if passwordHidden {
//     $('password').
//   }
// }
