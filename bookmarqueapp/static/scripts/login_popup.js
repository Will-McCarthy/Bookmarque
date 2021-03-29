/**
1. click avatar button/icon
2. check cookie to see if logged in
  - if logged in go to profile page
  - else continue
3. blur page and show login popup
  - will always be the first page to popup
4. login branches to:
  - login
  - forget password
  - create account process
  - close popup

5. create account process
  - move through multiple pages of forms until everything is submitted
  - js validation for forms
    - update button on payment and shipping with "Next" if they get filled out
6. at very end when all data has been entered
  - db updated with flask somehow, I guess with a "POST"
  - send out verification email
**/


/* enum with tab associations */
const tabs = {
  NONE: -1,
  LOGIN: 0,
  REGISTRATION: 1,
  PAYMENT: 2,
  ADDRESS: 3,
  CONFIRMATION: 4
}

var tab = tabs.NONE; //popup menu tab currently being rendered

/*
 * Abbreviated way to grab HTML elements by their ID.
 * @param   {String}  id  Element id in the HTML tag.
 * @return  {Object}      Element with corresponding id.
 */
var $ = function(id) {
  return document.getElementById(id);
} //$

function blurOverlay() {
  $("overlay").style.display = "block";
} //blurOverlay

/*
 * Check if the current user is logged in based on session cookies
 * in order to redirect to profile page. Else create login/registration popup.
 * @TODO implement cookie checking and validation
 */
var checkUserLoginStatus = function() {

  let loggedIn = false; //FOR TESTING

  if (loggedIn) {
    //~redirect to users profile page~
  } else {
    switchTab(tabs.LOGIN); //update tab to login
    blurOverlay(); //blur background and remove access
  } //if else
} //checkuserLoginStatus

/*
 * Switch current tab with parameter tab.
 */
function switchTab(newTab) {

  if (tab != tabs.NONE) {
    $('tab-' + tab).style.display = "none"; //remove old tab
  } //if

  $('tab-' + newTab).style.display = "flex"; //display updated tab
  tab = newTab;
} //switchTab

/*
 * Add event listeners to elements on window.
 */
window.onload = function() {
  var profileBtn = $('profile-button');
  profileBtn.onclick = checkUserLoginStatus;

  var registrationBtn = $('registration-button');
  registrationBtn.onclick = function() {
    switchTab(tabs.REGISTRATION);
  };

  //BROKEN :(
  var continueBtns = document.getElementByClassName("continue-registration-button");
  for (var i = 0; i < continueRegistrationBtn.length; i++) {
    continueBtns[i].onclick = function() {
      switchTab(tab + 1);
    };
  } //for
} //window.onload
