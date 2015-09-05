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
                alert('made it here');
                if (result === 'success') {
                    alert('door open');
                } else {
                    alert('door closed')
                }
            }
        });
    });
});
