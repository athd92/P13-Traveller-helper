$(document).ready(function() {
    $('#maploader').hide()

});




$("#agree-btn").click(function() {
    $("#cookie-bar").hide();
    $("#agree-btn").hide();
});

$("#myModal").on("shown.bs.modal", function() {
    console.log("MODAL LAUNCH");
    $("#myInput").trigger("focus");
});

$("#del-post").click(function() {
    console.log('click')
    console.log($("#del-post").attr('data'))
        // let entry = {
        //     post_is: $("#post_id").text(),
        // };
        // console.log("ENTRY : " + entry.aliment_id);
        // $.ajax({
        //     type: "POST",
        //     url: `${window.origin}/send_infos/`,
        //     data: {
        //         aliment_id: entry.aliment_id,
        //         csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        //     },
        //     beforeSend: function() {
        //         console.log("before");
        //         $("#mail").hide();
        //         $("#sending").show();
        //     },
        //     complete: function() {
        //         console.log("after");
        //         $("#sending").hide();
        //     },

    //     success: function(data, textStatus) {
    //         console.log("SUCCESS AJAX");
    //         if (data.response == "ok") {
    //             $("#sent").show();
    //             $("#sent").click(false);
    //         } else {
    //             $("#sent").hide();
    //             $("#error").show();
    //         }
    //     },
    //     error: function(req, err) {
    //         $("#sent").hide();
    //         console.log("Ajax request failed: " + err + req);
    //         $("#error").show();
    //     },
    // });
});