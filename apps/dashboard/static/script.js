$(document).ready(function(){
    console.log("Script linked")

    $('form').submit(function(event){
        console.log("Submitting form")
        
        form = $(this);
        formData = $(this).serializeArray();
        console.log(formData);
        emailIndex = NaN;

        for (var i=0; i<formData.length; i++){
            if (formData[i].name == 'email'){
                emailIndex = i;
                break;
            }
        }

        if(emailIndex!=NaN){
            $.get( "/duplicate_email", {'email': formData[emailIndex].value}, function(data){
                if (data['duplicate'] == true){
                    console.log("1*************************")
                    console.log("Email is already in use")
                    $(this).children('input').attr("value", "")

                    $('label[for="email"]').siblings(".invalid-feedback").text("Email already exists");
                }
                check(form);
            });
        }

        if ( !$(this)[0].checkValidity() ){
            console.log("2*************************")
            event.preventDefault();
            event.stopPropagation();
        }

        $(form).addClass('was-validated');
        
        return false;
    });





});