$('#getinfos').click(function(){

        let search = $('#search_input').val()
        console.log(search)

        $.ajax({
          type: "POST",
          url: `${window.origin}/get_infos/`,
          data: {
            'search': search,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
          },
          beforeSend: function () {
            console.log("before");
           
          },
          complete: function () {
           
          },
      
          success: function (data) {
        
          },
          error: function (req, err) {
            $("#sent").hide();
            console.log("Ajax request failed: " + err + req);
            $("#error").show();
          },
        });
    
    
});