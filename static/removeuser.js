$(document).ready(function () {
$('i').click(function() {
    console.log('hi');
    var userID = $(this).data("id");
    var data = {
        'userID' : userID
    }
    var selector = $(this);

    $.ajax({
        type : "POST",
        url : "/removeuser/",
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
          $('.accordian_' + userID).remove();
          $('.notification').remove();
          $( "nav" ).append( '<h2 class="notification success">User Removed!</h2>' );
        }
    });
});
});
