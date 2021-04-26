




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

} //toggleStarFilter
