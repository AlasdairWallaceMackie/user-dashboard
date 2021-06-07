$(document).ready(function(){
    console.log("Script linked")

    $('.alert').fadeIn(500).removeClass('d-none');

    $('form').submit(function(event){
        console.log("Submitting form")

        if ( $('#password').val() != $('#confirm').val() ){
            $('#confirm').siblings('.invalid-feedback').text("Password doesn't match");
            $('#confirm').val("");
        }

        if ( !$(this)[0].checkValidity() ){
            event.preventDefault();
            event.stopPropagation();
            console.log("Form is invalid")
            $(this).addClass('was-validated');
        
            return false;
        }
        else{
            console.log("Form passed validation!")
            
            // var path = window.location.pathname.replace("/", "%2F")
            // Forward slash = %2F
            // formData += `&current_url=${path}`

            // if (window.location.pathname != ("/register" || "/signin") )
            
            if ( /^\/users\/\d+$/.test(window.location.pathname) ){
                
                var formData = $(this).serialize()
                console.log(formData)
                var postURL = "post_message"

                $.ajax({
                    url: postURL,
                    method: "POST",
                    data: formData,
                    success: function(){
                        $.get(
                            "/newest_post",
                            function(data){
                                var output = ""
                                if (data.class == 'Message')
                                    output = ``
                                else if (data.class == 'Comment')
                                    output = ``

                                $(this).before(output)
                            },
                        )
                    }
                })

                // $.post(
                //     postURL,
                //     formData,
                //     function(){
                //         console.log("Submitting form via jQuery")
                //     }
                // )
            }

        }
    });







});