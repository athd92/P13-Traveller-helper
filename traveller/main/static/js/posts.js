$(document).ready(function() {
    $("#flagimg").hide("slide", { direction: "left" }, 1000);
});

$("#agree-btn").click(function() {
    $("#cookie-bar").hide();
    $("#agree-btn").hide();
});

$("#myModal").on("shown.bs.modal", function() {
    console.log("MODAL LAUNCH");
    $("#myInput").trigger("focus");
});