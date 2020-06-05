$(document).ready(function() {
    $("#maploader").hide();
});

$("#agree-btn").click(function() {
    $("#cookie-bar").hide();
    $("#agree-btn").hide();
});

$("#myModal").on("shown.bs.modal", function() {
    console.log("MODAL LAUNCH");
    $("#myInput").trigger("focus");
});


$(".first-delete").click(function() {

    var post_id = $(this).data("id");

    $("#DeleteModalCenter").modal()

    $('#del-post').click(function() {
        deletePost(post_id);
    })
});






function deletePost(post_id) {
    $.ajax({
        type: "POST",
        url: `${window.origin}/delete_post/`,
        data: {
            post_id: post_id,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        beforeSend: function() {

        },
        complete: function() {

        },

        success: function(data, textStatus) {

            console.log(data)
            location.reload();
        },
        error: function(req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    })
};




$(".first-message").click(function() {
    var post_ref = $(this).data("id");
    var message = $("#message-text").val()
    $('#new-message').click(function() {
        sendMessage(message, post_ref);
    });
});

function sendMessage(message, post_ref) {

    $.ajax({
        type: "POST",
        url: `${window.origin}/send_message/`,
        data: {
            message: message,
            post_ref: post_ref,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        beforeSend: function() {

        },
        complete: function() {

        },

        success: function(data, textStatus) {
            console.log(data)
            location.reload();
        },
        error: function(req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    })
}