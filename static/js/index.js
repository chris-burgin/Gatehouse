$(document).ready(function () {
    //Toggle Door
    $('.button').click(function() {
        event.preventDefault();
        $.ajax({
            type : "POST",
            url : "/toggledoor/",
            success: function(result) {
                //True: open
                //False: closed
                if (result === true) {
                    // Change door status message to open
                } else {
                    // Change door status message to closed
                }
            }
        });
    });
});
