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

function toggleOverlay() {
  $("overlay").style.display = ($("overlay").style.display == "block") ? "none" : "block";
} //toggleOverlay

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
    toggleOverlay(); //blur background and remove access
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
 * Check form for completeness and correctness.
 * Display error messages on incorrect or empty fields.
 * @return boolean for form status
 */
function validateForm() {

  switch (tab) {
    case tabs.REGISTRATION:

      let completeness = true;
      let inputFields = $('tab-' + tab).getElementsByTagName('input');

      //if any field is not filled in set completness to false and display error message
      for (let i = 0; i < inputFields.length; i++) {
        if (inputFields[i].value == '') completeness = false;
        //<display error message here>

      } //for

      return completeness;

      break;
    case tabs.PAYMENT:

      // check if anything is filled in, if nothing then change button back to 'skip for now' and return true
      //
      // if something is filled in check that everything is
      // change button to say save
      break;
    case tabs.ADDRESS:
      break;
  } //switch
  return true;
} //validateForm

/*
 * Change value of hidden skip field for corresponding tab to true.
 */
function skip() {
  switch (tab) {
    case tabs.PAYMENT:
      $('payment-skipped').value = true;
      break;
    case tabs.ADDRESS:
      $('shipping-skipped').value = true;
      break;
  } //switch
} //skip

/*
 * Add event listeners to elements on window.
 */
window.onload = function() {

  //button which either takes user to login/registration popup or to profile management
  let profileBtn = $('profile-button');
  profileBtn.onclick = checkUserLoginStatus;

  //button which takes user to registration form
  let registrationBtn = $('registration-button');
  registrationBtn.onclick = function() {
    switchTab(tabs.REGISTRATION);
  };

  //functionality for buttons to iterate through registration form
  let continueBtns = document.getElementsByClassName('continue-registration-button');
  for (let i = 0; i < continueBtns.length; i++) {
    continueBtns[i].onclick = function() {
      if (validateForm()) {
        switchTab(tab + 1);
      }
    };
  } //for

  //skip buttons will not validate fields but instead clear them
  let skipBtns = document.getElementsByClassName('skip');
  for (let i = 0; i < skipBtns.length; i++) {
    skipBtns[i].onclick = function() {
      skip();
      switchTab(tab + 1);
    };
  } //for

  //close popup button functionality
  let closeBtns = document.getElementsByClassName('close-popup-button');
  for (let i = 0; i < closeBtns.length; i++) {
    closeBtns[i].onclick = function() {
      toggleOverlay();
      switchTab(tabs.NONE);
    };
  } //for


} //window.onload
