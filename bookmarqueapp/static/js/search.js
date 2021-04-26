var results = document.getElementsByClassName('search-card');

var $ = function(id) {
  return document.getElementById(id);
} //$


var toggleStarFilter = function(star) {
  let num = parseInt(star.id.charAt(5)); //the number of the star in the order
  $('rating-filter').value = num; //set hidden field value to the star clicked

  $('star-' + 1).innerHTML = "hey";
  /* change what stars look like by updating every star up to num as filled and after as blank */
  for (let i = 1; i <= 5; i++) {
    $('star-' + i).innerHTML = (i <= num) ? '★' : '☆';
  } //for

  filterResultsShown();
} //toggleStarFilter


var checkPriceRange = function() {
  let min = $('price-min-filter');
  let max = $('price-max-filter');

  if ((min.value != "") & (max.value != "")) {
    min.max = parseInt(max.value) - 1;
    max.min = parseInt(min.value) + 1;

    if (min.value >= max.value) {
      max.value = parseInt(min.value) + 1;
    } //if
  } else {
    min.max = "";
    max.min = 0;
  } //else

  filterResultsShown();
} //checkPriceRange


var filterResultsShown = function() {
  let priceMin = $('price-min-filter');
  let priceMax = $('price-max-filter');
  let starMin = $('rating-filter');
  let inStock = $('in-stock').checked;

  let numResultsMessage = $('num-results-message');

  results = document.getElementsByClassName('search-card');
  for (let i = 0; i < results.length; i++) {
    results[i].style.display = "flex";
  }

  let numShown = results.length;

  /* price filters */
  let prices = document.getElementsByClassName('price-value');
  for (let i = 0; i < prices.length; i++) {
    let visible = true;

    if (((priceMin.value != "" && parseInt(prices[i].value) < parseInt(priceMin.value)))
      || ((priceMax.value != "" && parseInt(prices[i].value) > parseInt(priceMax.value)))) {
        prices[i].parentElement.style.display = "none";
        numShown--;
    } //if
  } //for

  /* ratings filter */
  let ratings = document.getElementsByClassName('rating-value');
  for (let i = 0; i < ratings.length; i++) {

    //check if already filtered out
    if (ratings[i].parentElement.style.display == "flex") {

      let x = parseInt(starMin.value);
      let y = parseInt(ratings[i].value);
      if (x > y) {
        ratings[i].parentElement.style.display = "none";
        numShown--;
      } //if
    } //if
  } //for

  /* in stock filter */
  let stocks = document.getElementsByClassName('stock-value');
  for (let i = 0; i < stocks.length; i++) {
    if (stocks[i].parentElement.style.display == "flex") {
      if (inStock && !(stocks[i].checked)) {
        stocks[i].parentElement.style.display = "none";
        numShown--;
      } //if
    } //if
  } //if

  /* message */
  numResultsMessage.innerHTML = "Showing ".concat(numShown).concat(" results");

} //filterResultsShown
