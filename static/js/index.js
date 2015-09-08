$(document).ready(function () {

    //Toggle Door
    $('.button').click(function() {
        event.preventDefault();
        $.ajax({
            type : "POST",
            url : "/toggledoor/",
            success: function(result) {

            }
        });
    });

    // checks door status
    function doorLoop() {
        setTimeout(function(){
            checkDoor();
            doorLoop();
        }, 5000);
    }

    var doorStatus = $('.doorstatus');
    if (!doorStatus.hasClass('disabled')){
        checkDoor();
        doorLoop();
    }

    //Check Door
    function checkDoor(){
        $.ajax({
            type : "POST",
            url : "/doorstatus/",
            success: function(result) {
                if (result === 'unknown') {
                    doorStatus.text('Door In Motion');
                } else if (result === "open") {
                    doorStatus.text('Door Open');
                } else if (result === "closed") {
                    doorStatus.text('Door Closed');
                }
            }
        });
    }

});
