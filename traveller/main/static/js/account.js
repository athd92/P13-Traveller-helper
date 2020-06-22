$(document).ready(function() {

    $("#but_upload").click(function() {
        var fd = new FormData();
        var files = $('#file')[0].files[0];
        fd.append('file', files);
        getBase64(files, fd)
    });
});






function getBase64(file) {

    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function() {
        console.log(reader.result);
        var img64 = reader.result
        console.log("IMAGE")
        console.log(img64)
        console.log(typeof img64)

        $.ajax({
            url: `${window.origin}/upload_img/`,
            type: 'post',
            headers: { "X-CSRFToken": getCookie("csrftoken") },
            data: { img64: img64 },
            dataType: 'json',
            beforeSend: function() {
                console.log("before")
            },
            complete: function() {

            },
            success: function(response) {
                if (response != 0) {
                    $("#img").attr("src", response);
                    $(".preview img").show(); // Display image element
                    window.location.reload()
                } else {
                    alert('file not uploaded');
                }
            },
            error: function(req, err) {
                $("#sent").hide();
                console.log("Ajax request failed: " + err + req);
                $("#error").show();
            },
        });



        $('img').attr("src", img64)
        return img64
    };
    reader.onerror = function(error) {
        console.log('Error: ', error);
    };
}

function getCookie(c_name) {
    if (document.cookie.length > 0) {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1) {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start, c_end));
        }
    }
    return "";
}