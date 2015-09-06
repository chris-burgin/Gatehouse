$(document).ready(function () {

    // checks door status
    function checkDoor() {
        setTimeout(function(){
            $.ajax({
                type : "POST",
                async: false,
                url : "/doorstatus/",
                success: function(result) {
                    if (result === 'unknown') {
                        alert ('unknown');
                    } else if (result === "open") {
                        alert ('open');
                    } else if (result === "closed") {
                        alert ('closed');
                    }
                }
            });
            checkDoor();
        }, 5000);
    }
    checkDoor();

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
