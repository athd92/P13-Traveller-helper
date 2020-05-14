// $("#getinfos").click(function() {
//     // let search = $("#exampleFormControlSelect1 option:selected").attr('id');
//     let search = $('option:selected').attr('id')
//     console.log(search);

//     $.ajax({
//         type: "GET",
//         url: `${window.origin}/posts/` + search,
//         data: {
//             search: search,
//             csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
//         },
//         beforeSend: function() {
//             console.log("before");
//         },
//         complete: function(data) {},

//         success: function(data) {

//             window.location.replace(`${window.origin}/posts/` + data.country_id);

//         },
//         error: function(req, err) {
//             $("#sent").hide();
//             console.log("Ajax request failed: " + err + req);
//             $("#error").show();
//         },
//     });
// });

$("#agree-btn").click(function() {
    $("#cookie-bar").hide();
    $("#agree-btn").hide();
});