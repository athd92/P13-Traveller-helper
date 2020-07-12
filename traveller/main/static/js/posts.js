$(document).ready(function () {
    $("#maploader").hide();
});


$('.open-map').click(function () {
    var city = $(this).data("id");
    console.log(city)
    displayMap(city)
    $('#close-map').click(function () {
        console.log('CLOSE')
        $(".divmap").empty();
    });

})




$("#agree-btn").click(function () {
    $("#cookie-bar").hide();
    $("#agree-btn").hide();
});

$("#myModal").on("shown.bs.modal", function () {
    $("#myInput").trigger("focus");
});


$(".first-delete").click(function () {
    var post_id = $(this).data("id");
    $("#DeleteModalCenter").modal()
    $('#del-post').click(function () {
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
        beforeSend: function () {},
        complete: function () {},
        success: function (data, textStatus) {
            console.log(data)
            location.reload();
        },
        error: function (req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    })
};




$(".first-message").on("click", function () {
    var post_ref = $(this).data("id");

    $('#new-message').click(function () {

        var message = $("#message-text").val();
        console.log(message)
        console.log(post_ref)
        sendMessage(message, post_ref);
    });
});

function sendMessage(message, post_ref) {
    console.log(message)

    $.ajax({
        type: "POST",
        url: `${window.origin}/send_message/`,
        data: {
            message: message,
            post_ref: post_ref,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
        },
        beforeSend: function () {

        },
        complete: function () {

        },

        success: function (data, textStatus) {
            console.log(data)
            toastr.success('Message sent!')
            $('#messageModal').modal('toggle');
        },
        error: function (req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    })
}

$(".modify-modal").click(function () {

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
        beforeSend: function () {},
        complete: function () {},

        success: function (data, textStatus) {
            displayModifyModal(data)

        },
        error: function (req, err) {
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
        beforeSend: function () {

        },
        complete: function () {

        },

        success: function (data) {
            console.log(data)
            $('#displayMap').modal()
            $('.divmap').append('<div id="map"></div>');
            initMap();

        },
        error: function (req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
        },
    })
}











var map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: {
            lat: -34.397,
            lng: 150.644
        },
        zoom: 8
    });
}





// function initMap(latitude, longitude, data) { // initialisation of googlemaps   
//     // map options    
//     var options = {
//         zoom: 11,
//         center: { lat: latitude, lng: longitude },
//     }

//     // new map
//     var map = new google.maps.Map(document.getElementById('map'), options);

//     // add marker
//     var marker = new google.maps.Marker({
//         position: { lat: latitude, lng: longitude },
//         map: map
//     });

//     var infowindow = new google.maps.InfoWindow();
//     infowindow.setContent(data.address);
//     infowindow.open(map, marker);


// };




// map function ajax
$(document).ready(function () {
    var map = null;
    var myMarker;
    var myLatlng;

    function initializeGMap(lat, lng) {
        myLatlng = new google.maps.LatLng(lat, lng);

        var myOptions = {
            zoom: 12,
            zoomControl: true,
            center: myLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };

        map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

        myMarker = new google.maps.Marker({
            position: myLatlng
        });
        myMarker.setMap(map);
    }

    // Re-init map before show modal
    $('#myModal').on('show.bs.modal', function (event) {

        const button = $(event.relatedTarget);
        const city = button.data('city');
        const country = button.data('country');

        $.ajax({
            type: "POST",
            url: `${window.origin}/get_geocode/`,
            data: {
                city: city,
                country: country,
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                console.log(data.coords)
                let lat = String(data.coords.lat).slice(0, 6)
                let lng = String(data.coords.lng).slice(0, 6)
                lat = parseFloat(lat)
                lng = parseFloat(lng)

                initializeGMap(lat, lng);
                $("#location-map").css("width", "100%");
                $("#map_canvas").css("width", "100%");
                // Trigger map resize event after modal shown
                $('#myModal').on('shown.bs.modal', function () {
                    google.maps.event.trigger(map, "resize");
                    map.setCenter(myLatlng);
                });

            },
            error: function (req, err) {
                $("#sent").hide();
                console.log("Ajax request failed: " + err + req);
                $("#error").show();
            },
        })


    });

});