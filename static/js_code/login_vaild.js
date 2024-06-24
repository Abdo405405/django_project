document.addEventListener('DOMContentLoaded', function() {
    let myLogBtn = document.querySelector(".login-form .btn-log");
    let emailInput = document.querySelector(".login-form .email-input");
    let passInput = document.querySelector(".login-form .pass-input");
    let emailRequired = document.querySelector(".login-form .email-empty");
    let passRequired = document.querySelector(".login-form .pass-empty");
    // let succMessage = document.querySelector(".success-message");

    myLogBtn.addEventListener("click", function (e) {
        let errorMessages = document.querySelectorAll(".error-masge");
        errorMessages.forEach(message => {
            message.style.display = "none";
        });

        if (emailInput.value === "" && passInput.value === "") {
            emailRequired.style.display = "block";
            passRequired.style.display = "block";
            e.preventDefault();
        } else {
            if (emailInput.value === "" && passInput.value !== "") {
                emailRequired.style.display = "block";
                e.preventDefault();
            } else if (emailInput.value !== "" && passInput.value === "") {
                passRequired.style.display = "block";
                e.preventDefault();
            } 
            // else {
            //     // Show success message after 20 seconds
            //     // setTimeout(function() {
            //         succMessage.style.display = "block";
            //     // }, 20000); // 20 seconds in milliseconds
            // }
        }
    });
});
