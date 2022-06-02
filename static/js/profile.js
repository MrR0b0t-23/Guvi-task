(function() {
    'use strict';
    window.addEventListener('load', function() {
        // Get the forms we want to add validation styles to
        var forms = document.getElementsByClassName('needs-validation');
        // Loop over them and prevent submission
        var validation = Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

function forgetpassword() {
    var x = document.getElementById("pwd");
    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

$(document).ready(function() {
    $('#profileform').on('sumbit', function(event) {
        event.preventDefault();

        $.ajax({
            data: {
                fname: $('#inputfname').val(),
                lname: $('#inputlname').val(),
                email: $('#inputemail').val(),
                cnumber: $('#inputcnumber').val(),
                age: $('#inputage').val(),
                degree: $('#inputdegree').val(),
                dept: $('#inputdept').val(),
                poyear: $('#inputpoyear').val(),
                rnumber: $('#inputrnumber').val(),
                cgpa: $('#inputcgpa').val(),
                intro: $('#inputintro').val(),
                sslcschool: $('#inputsslcschool').val(),
                sslcprecent: $('#inputsslcprecent').val(),
                sslcyear: $('#inputsslcyear').val(),
                hscschool: $('#inputhscschool').val(),
                hscprecent: $('#inputhscprecent').val(),
                hscyear: $('#inputhscyear').val(),
                website: $('#inputwebsite').val(),
                github: $('#inputgithub').val()
            },
            type: "POST",
            url: '/profile'
        });

    });
});