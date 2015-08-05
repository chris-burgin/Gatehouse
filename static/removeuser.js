$(document).ready(function () {
$('i').click(function() {
    console.log('hi');
    var data = {
        'userID' : $(this).data("id")
    }

    $.ajax({
        type : "POST",
        url : "/removeuser/",
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
           console.log(result);
        }
    });
});
});
