$(document).ready(function () {
    //Remove User
    $('.fa-trash-o').click(function() {
        var userID = $(this).data("id");
        var data = {
            'userID' : userID
        };
        var selector = $(this);

        $.ajax({
            type : "POST",
            url : "/removeuser/",
            data: JSON.stringify(data, null, '\t'),
            contentType: 'application/json;charset=UTF-8',
            success: function(result) {
                $('.accordian_' + userID).remove();
                $('.notification').remove();
                if (result == "success") {
                    notification('success','User Updated!');
                } else {
                    notification('success','Failed To Update User.');
                }
            }
        });
    });

    //Check Password Length
    $( ".edit-user .password, .edit-user .username" ).keyup(function() {
        var selector = $(this).attr("class");
        var username;
        var password;
        if (selector == 'password') {
            password = $(this);
            username = $(this).parent('.edit-user').find('.username');
        } else {
            username = $(this);
            password = $(this).parent('.edit-user').find('.password');
        }
        var updateValid = true;
        if (password.val().length > 5) {
            password.removeClass('error');
        } else {
            updateValid = false;
            password.addClass('error');
        }
        if (username.val().length > 2) {
            username.removeClass('error');
        } else {
            updateValid = false;
            username.addClass('error');
        }

        if (updateValid === true) {
            $(this).parent('.edit-user').find('.update-user').prop('disabled', false);
        } else {
            $(this).parent('.edit-user').find('.update-user').prop('disabled', true);
        }
    });
});

//Extra Functions
function notification(type, message) {
    $( "nav" ).append( '<h2 class="notification' + type + '">' + message + '</h2>' );
}
