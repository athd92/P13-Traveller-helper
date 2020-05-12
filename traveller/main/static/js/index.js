$("#getinfos").click(function() {
    let search = $("#exampleFormControlSelect1 option:selected").text();
    // let search = $('#search_input').val()
    console.log(search);

    $.ajax({
        type: "POST",
        url: `${window.origin}/get_infos/`,
        data: {
            search: search,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        beforeSend: function() {
            console.log("before");
        },
        complete: function(data) {},

        success: function(data) {
            console.log(data);
            window.location.replace(`${window.origin}/posts/`);
        },
        error: function(req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    });
});

$("#agree-btn").click(function() {
    $("#cookie-bar").hide();
    $("#agree-btn").hide();
});