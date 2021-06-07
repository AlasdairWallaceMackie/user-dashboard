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
                    console.log("Posting message/comment")
                    var formData = $(this).serialize()
                    console.log(formData)
                    userID = window.location.pathname.split("/")[2]
                    console.log(userID)
                    var postURL = `/users/${userID}/post_message`
                    console.log("Post URL: " + postURL)
                    var form = $(this)
    
                    $.ajax({
                        url: postURL,
                        method: "POST",
                        data: formData,
                        success: function(){
                            $.get(
                                "/newest_post",
                                {'user_id': userID},
                                function(data){
                                    console.log("DATA:")
                                    console.log(data)
                                    console.log(typeof data)
                                    if(data.includes(`class="post"`)){
                                        //Class has to be named 'post' in order to not interfere with Django messages
                                        console.log("Rendering message")
                                        $(form).after(data);
                                        $(form).next().hide();
                                        $(form).next().slideDown(250);
                                    }
                                    else if(data.includes(`class="comment"`)){
                                        console.log("Rendering comment")
                                        $(form).before(data);
                                        $(form).prev().hide();
                                        $(form).prev().slideDown(250);
                                    }
                                    $(form).children().val("")
                                },
                            )
                        }
                    })
                }
                return false;
            }
        });

});