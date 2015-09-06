$(document).ready(function () {

    // checks door status
    function doorLoop() {
        setTimeout(function(){
            checkDoor();
            doorLoop();
        }, 5000);
    }
    doorLoop();

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

    //Check Door
    function checkDoor(){
        $.ajax({
            type : "POST",
            async: false,
            url : "/doorstatus/",
            success: function(result) {
                if (result === 'unknown') {
                    $('.doorstatus').text('Door In Motion');
                } else if (result === "open") {
                    $('.doorstatus').text('Door Open');
                } else if (result === "closed") {
                    $('.doorstatus').text('Door Closed');
                }
            }
        });
    }

});
