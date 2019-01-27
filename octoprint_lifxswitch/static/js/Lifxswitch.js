$(function() { 
    $('#btnFindLights').on('click', function() {

        var accessToken = $("#txtAccessToken").val();
        var payload = {"access_token": accessToken};
        
        try {
            OctoPrint.simpleApiCommand("lifxswitch", "list_lights", payload)
                .done(function(response) {
                    // do something with the response
                    console.log(response);
                });            
        } catch (error) {
            console.log('error '+ error);
        }

    });
});     