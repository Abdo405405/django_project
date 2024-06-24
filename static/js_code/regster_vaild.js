// start register form validation 
//start declaration
      let firstName =  document.querySelector("#first_name");
      let registerForm =  document.querySelector(".register-form");
      let lastName  = document.querySelector("#last_name"); 
      let setUserName  = document.querySelector("#username"); 
      let emailInput = document.querySelector("#email");  
      let newPassword =document.querySelector("#password");
      let confirmPass =document.querySelector("#confirm_password"); 
      let birthDate = document.querySelector("#birth_field"); 
      let userGender = document.querySelector("#gender");
      let registerBtn =document.querySelector(".regst-btn");
      let emailValue = emailInput.value.trim();
//end declaration

//limitation
firstName.maxLength = 30;
lastName.maxLength = 30;
setUserName.maxLength = 30;

 //create required message
registerBtn.addEventListener("click", function(e) {
     e.preventDefault();
     let newUser = {
       name:"",
       password:""
     };
     let allFields = document.querySelectorAll(".fields");
     let errorMessages = document.querySelectorAll(".register-box .error-masge");
    errorMessages.forEach(error => error.style.display = "none");
    allFields.forEach(f => f.classList.remove("error"));
     allFields.forEach((item) =>{
        errorMessages.forEach((error) => {
        let errorField = error.dataset.field;
           if(item.id === firstName.id 
           && errorField === firstName.id){
              let firstNameValue = firstName.value.trim();
               if(firstNameValue === ""){
                   error.style.display = "block";
                   firstName.classList.add("error");
               }
           }
           
           if(item.id === lastName.id && 
           errorField === lastName.id){
              let lastNameValue = lastName.value.trim();
               if(lastNameValue === ""){
                   error.style.display = "block";
                   lastName.classList.add("error");
               }
           }
           
           if(item.id === setUserName.id && 
           errorField === setUserName.id){
              let userNameValue = setUserName.value.trim();
               if(userNameValue === ""){
                   error.style.display = "block";
                   setUserName.classList.add("error");
               }
               else {
                  newUser.name = userNameValue;
               }
           }
           
           if(item.id === birthDate.id && 
           errorField === birthDate.id){
              let birthDateValue = birthDate.value;
               if(birthDateValue === ""){
                   error.style.display = "block";
                   birthDate.classList.add("error");
               }
           }
           
           if(item.id === userGender.id &&
            errorField === userGender.id){
              let userGenderValue = userGender.value;
               if(userGenderValue === ""){
                   error.style.display = "block";
                   userGender.classList.add("error");
               }
           }
           
           if(item.id === newPassword.id && 
            errorField === newPassword.id){
              checkPassword(error ,newUser);
            }
            
           if(item.id === confirmPass.id &&
           errorField === confirmPass.id){
               confirmPassCheck(error)
           }
           
           if(item.id === emailInput.id && 
           errorField === emailInput.id ){
              checkEmail(error);
           }
        });
    });
   let errorClasses = document.querySelectorAll(".error");
    if(errorClasses.length === 0){
       registerBtn.innerHTML = `<i class="fa-solid fa-circle-notch fa-spin"></i>`;
       // newPassword.type = "password";
//        confirmPass.type = "password";
      document.querySelector("#pass-toggle-btn").click();
      document.querySelector("#confirm-toggle-btn").click();
      if(newUser.name !== "" && newUser.password !== ""){
       window.localStorage.clear();
       window.localStorage.setItem("user",JSON.stringify(newUser))
      }
      setTimeout(function(){
        registerForm.submit();
       },1000);
       setTimeout(function(){
       window.location ="login.html";
     },1200);
     }
});

//check functions
function checkPassword (error,user){
  const passPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
  let passValue = newPassword.value;
    if(passValue === ""){
        error.style.display = "block";
        newPassword.classList.add("error");
     }
    
    else if( passValue !== "" && 
    !passPattern.test(passValue)){
      error.style.display = "block";
      newPassword.classList.add("error");
    }
    else {
      user.password = passValue;
      return true ;
    }
}
function checkEmail (error){
 const emaiPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
  let emailValue = emailInput.value.trim();
      if(emailValue === ""){
        error.style.display = "block";
        emailInput.classList.add("error");
        return false;
      }
      else if(emailValue !== "" && 
      !emaiPattern.test(emailValue)){
            error.style.display = "block";
            emailInput.classList.add("error");
            return false;
      }
     else {
      return true ;
    }
}
function confirmPassCheck (error){
 const emaiPattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/;
  let confValue = confirmPass.value;
 if(confValue === "" || confValue !== newPassword.value){
   error.style.display = "block";
   confirmPass.classList.add("error");
   return false ;
 }
  else {
      return true ;
 }
}

//show /hide password btns
document.addEventListener('click', (e) => {
   if(e.target.id === "pass-toggle-btn"){
      if(e.target.classList.contains("fa-eye-slash")){
         e.target.classList.replace("fa-eye-slash","fa-eye");
         newPassword.type = "text";
       }
      else if(e.target.classList.contains("fa-eye")){
         e.target.classList.replace("fa-eye","fa-eye-slash");
         newPassword.type = "password";
       }
     }
});
document.addEventListener('click', (e) => {
   if(e.target.id === "confirm-toggle-btn"){
      if(e.target.classList.contains("fa-eye-slash")){
         e.target.classList.replace("fa-eye-slash","fa-eye");
         confirmPass.type = "text";
       }
      else if(e.target.classList.contains("fa-eye")){
         e.target.classList.replace("fa-eye","fa-eye-slash");
         confirmPass.type = "password";
       }
    }
});
