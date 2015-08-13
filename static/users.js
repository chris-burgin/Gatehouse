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
                    notification('success','User Removed!');
                } else {
                    notification('success','Failed To Remove User.');
                }
            }
        });
    });

    //Check Password Length
    $( ".edit-user .password, .edit-user .username" ).on("input", function() {
        var selector = $(this).attr("class");
        var username;
        var password;
        var submitButton = $(this).parent('.edit-user').find('.button');
        alert(selector);
        if (selector.indexOf('password') != -1) {
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
            if (password.is(":focus")) {
                password.addClass('error');
            }

        }
        if (username.val().length > 2) {
            username.removeClass('error');
        } else {
            updateValid = false;
            if (username.is(":focus")) {
                username.addClass('error');
            }
            submitButton.addClass('disabled');
        }

        if (updateValid === true) {
            submitButton.prop('disabled', false);
            submitButton.removeClass('disabled');
        } else {
            submitButton.prop('disabled', true);
            submitButton.addClass('disabled');
        }
    });
});

//Extra Functions
function notification(type, message) {
    $( "nav" ).append( '<h2 class="notification ' + type + '">' + message + '</h2>' );
}
