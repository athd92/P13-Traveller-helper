$("#agree-btn").click(function() {
    $("#cookie-bar").hide();
    $("#agree-btn").hide();
});


$(document).ready(function() {
    $(".card").addClass("delay-1s");
});


$('.random-img').click(function() {
    var query = $(this).data("id");
    console.log(query)
    $.ajax({
        type: "POST",
        url: `${window.origin}/get_img/`,
        data: {
            query: query,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        beforeSend: function() {
            $('#imgModal').modal('show')
            $('#spinner').attr("hidden", false);
            $('#imgModal').hide()
            $("#randomImg").attr("hidden", true);
        },
        complete: function() {
            //$('#spinner').hide()
        },

        success: function(data, textStatus) {
            console.log(data)
            $("#randomImg").empty()
            $('#randomImg').attr('src', data.result)
            $('#spinner').attr("hidden", true);
            $("#randomImg").attr("hidden", false);
            $('#imgModal').show()
        },
        error: function(req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    })
})