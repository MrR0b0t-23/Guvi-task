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

$('#signupform').on('sumbit', function(event) {

    event.preventDefault();
    $.ajax({
        data: {
            fname: $('#fname').val(),
            lname: $('#lname').val(),
            email: $('#email').val(),
            mnumber: $('#mnumber').val(),
            pwd: $('#pwd').val()
        },
        type: 'POST',
        url: '/'
    });

});