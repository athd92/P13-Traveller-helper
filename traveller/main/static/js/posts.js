$(document).ready(function() {
    $("#maploader").hide();

});


$('#open-map').click(function() {
    var city = $(this).data("id");
    console.log(city)
    displayMap(city)
})






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
        beforeSend: function() {},
        complete: function() {},
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

$(".modify-modal").click(function() {

    var post_id = $(this).data("id");

    // $("#DeleteModalCenter").modal()

    // $('#del-post').click(function() {
    //     deletePost(post_id);
    // })

    $.ajax({
        type: "POST",
        url: `${window.origin}/modify_post/`,
        data: {
            post_id: post_id,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        beforeSend: function() {},
        complete: function() {},

        success: function(data, textStatus) {
            displayModifyModal(data)

        },
        error: function(req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    })
});




function displayMap(city) {

    $.ajax({
        type: "POST",
        url: `${window.origin}/display_map/`,
        data: {
            city: city,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        beforeSend: function() {

        },
        complete: function() {

        },

        success: function(data) {
            console.log(data)
            $('#displayMap').modal()
            $('.divmap').append('<div id="map">' + 'map...' + '</div>');
            initMap(40000, 25000, data);
        },
        error: function(req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    })
}

















function initMap(latitude, longitude, data) { // initialisation of googlemaps   
    // map options    
    var options = {
        zoom: 11,
        center: { lat: latitude, lng: longitude },
    }

    // new map
    var map = new google.maps.Map(document.getElementById('map'), options);

    // add marker
    var marker = new google.maps.Marker({
        position: { lat: latitude, lng: longitude },
        map: map
    });

    var infowindow = new google.maps.InfoWindow();
    infowindow.setContent(data.address);
    infowindow.open(map, marker);


};