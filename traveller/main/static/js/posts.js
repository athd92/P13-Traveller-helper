$("#agree-btn").click(function() {
    $("#cookie-bar").hide();
    $("#agree-btn").hide();
});

$('#myModal').on('shown.bs.modal', function() {
    $('#myInput').trigger('focus')
})