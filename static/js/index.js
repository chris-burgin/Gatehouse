$(document).ready(function () {
    //Toggle Door
    $('.button').click(function() {
        event.preventDefault();
        $.ajax({
            type : "POST",
            async: false,
            url : "/toggledoor/",
            success: function(result) {

            }
        });
    });
});


// checks door status
setTimeout(function(){
    $.ajax({
        type : "POST",
        async: false,
        url : "/doorstatus/",
        success: function(result) {
            if (result === 'unknown') {
                alert ('unkown');
            } else if (result === "open") {
                alert ('open');
            } else if (result === "closed") {
                alert ('closed');
            }

        }
    });
}, 5000);
