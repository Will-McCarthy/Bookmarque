/* enum with tab associations */
const tabs = {
  NONE: -1,
  LOGIN: 0,
  REGISTRATION: 1,
  PAYMENT: 2,
  ADDRESS: 3,
  CONFIRMATION: 4,
  FORGOTPASSWORD: 5,
  EMAILSENT: 6
}

var tab = tabs.NONE; //popup menu tab currently being rendered

var emailformat = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
var phoneformat = /^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$/;
var zipformat = /(^\d{5}$)|(^\d{5}-\d{4}$)/;
var passwordformat = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

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
      return validateRegistration();
      break;
    case tabs.PAYMENT:
      return validatePayment();
      break;
    case tabs.ADDRESS:
      return validateAddress();
      break;
  } //switch
  return true;
} //validateForm

function validateRegistration() {
  let completeness = true;
  let inputFields = $('tab-' + tab).getElementsByTagName('input');

  //if any field is not filled in set completness to false and display error message
  for (let i = 0; i < inputFields.length; i++) {
    let field = inputFields[i];
    if (field.value == '') {
      completeness = false;
      field.style.border = 'solid .15rem red';

    //specialty cases for phone and email validation
    } else if ((field.name == 'phone' && !field.value.match(phoneformat)) ||
      (field.name == 'email' && !field.value.match(emailformat))) {

      completeness = false;
      field.style.border = 'solid .15rem red';
      field.value = 'Please use a valid format';

    //password validation
    } else if (field.name == 'password' && !field.value.match(passwordformat)) {
      completeness = false;
      field.style.border = 'solid .15rem red';
    } else {
      field.style.border = '';
    } //else
  } //for
  return completeness;
} //validateRegistration

function validatePayment() {
  let type = document.getElementsByName('cardType')[0];
  let number = document.getElementsByName('cardNumber')[0];
  let expMonth = document.getElementsByName('expMonth')[0];
  let expYear = document.getElementsByName('expYear')[0];
  let svc = document.getElementsByName('svc')[0];

  if (!checkCreditCard(number.value, type.value)) { //method defined in creditcard.js
    number.style.border = 'solid .15rem red';
    type.style.border = 'solid .15rem red';
    return false;
  }
  if (expMonth.value == "MM") {
    expMonth.style.border = 'solid .15rem red';
    return false;
  }
  if (expYear.value < 21 || expYear.value > 99) {
    expYear.style.border = 'solid .15rem red';
    return false;
  }
  if (isNaN(parseInt(svc.value)) || parseInt(svc.value) > 999 || parseInt(svc.value) < 0) {
    svc.style.border = 'solid .15rem red';
    return false;
  }
  return true;
} //validatePayment

function validateAddress() {
  let completeness = true;
  let inputFields = $('tab-' + tab).getElementsByTagName('input');
  //if any field is not filled in set completness to false and display error message
  for (let i = 0; i < inputFields.length; i++) {
    let field = inputFields[i];
    if (field.value == '') {
      completeness = false;
      field.style.border = 'solid .15rem red';
      //specialty cases for zipcode validation
    } else if (field.name == 'zip' && !field.value.match(zipformat)) {
      completeness = false;
      field.style.border = 'solid .15rem red';
    } else {
      field.style.border = '';
    } //else
  } //for
  return completeness;
}

function validatePassword() {
  let password = $('passwordReset');
  let passConfirm = $('passConfirm');
  if(password.value != passConfirm.value){
    password.style.border = 'solid .15rem red';
    passConfirm.style.border = 'solid .15rem red';
    return false;
  }
  if(!password.value.match(passwordformat)){
    password.style.border = 'solid .15rem red';
    passConfirm.style.border = 'solid .15rem red';
    return false;
  }
  return true;
}

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
  profileBtn.onclick = function() {
    switchTab(tabs.LOGIN); //update tab to login
    toggleOverlay(); //blur background and remove access
  };

  //button which takes user to registration form
  let registrationBtn = $('registration-button');
  registrationBtn.onclick = function() {
    switchTab(tabs.REGISTRATION);
  };

  let forgotPassBtn = $('forgot-password-button');
  forgotPassBtn.onclick = function() {
    switchTab(tabs.FORGOTPASSWORD);
  };

  // let resetPassBtn = $('reset-password-button');
  // resetPassBtn.onclick = function() {
  //   if(validatePassword()){
  //
  //   };
  // };

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
