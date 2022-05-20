$(document).ready( function () {
  $('#myTable').DataTable();
} );





/*$
$(document).ready(function($){


 var data_table_arr = [];

 for(var k = 0; k <=30; k++){

  data_table_arr.push([

    chance.id(),
    chance.name(),
    chance.email(),
    chance.date(),
    chance.action()


  ])
 }



$('#your-table').DataTable(
{

data: data_table_arr,
"lengthMenu" : [[10,25,50,100,-1],[10,25,50,100,"All"]],
"pageLength" :10,
columns:[
{title:'ID'},
{title:'Name'},
{title:'Email'},
{title:'Date'},
{title:'Action'},



],





});


  
});





















(document).ready(function(){
  // Initialize Tooltip
  $('[data-toggle="tooltip"]').tooltip(); 
  
  // Add smooth scrolling to all links in navbar + footer link
  $(".navbar a, footer a[href='#myPage']").on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {

      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (900) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 900, function(){
   
        // Add hash (#) to URL when done scrolling (default click behavior)
        window.location.hash = hash;
      });
    } // End if
  });
})
*/