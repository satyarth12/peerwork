

const usernameField=document.querySelector("#id_username");
const feedbackArea=document.querySelector(".invalid-feedback");
const emailField=document.querySelector("#id_email");
const emailfeedbackArea=document.querySelector(".emailfeedbackArea");
const usernamesuccess=document.querySelector(".usernamesuccess");
const showPassword=document.querySelector(".showPassword");
const passwordField=document.querySelector("#id_password1");



const handlePass = (e) => {

	if(showPassword.textContent=="SHOW"){
		showPassword.textContent="HIDE";

		passwordField.setAttribute("type", "text");
	}
	else{
		showPassword.textContent="SHOW";
		passwordField.setAttribute("type", "password");
	}


}


showPassword.addEventListener("click", handlePass);






emailField.addEventListener("keyup", (e) =>{

	const emailVal=e.target.value;

	emailField.classList.remove("is-invalid"); 
	emailfeedbackArea.style.display="none";

	if(emailVal.length>0){

		fetch("/validate-email/",{
		body: JSON.stringify({email:emailVal}),
		method:"POST",
	})
		.then((res) => res.json())
		.then((data) => {
			console.log("data",data);
			if(data.email_error){
				emailField.classList.add("is-invalid");
				emailfeedbackArea.style.display="block";
				emailfeedbackArea.innerHTML= data.email_error;

			}
		});

	}
});






usernameField.addEventListener("keyup", (e) =>{
	
	const usernameVal=e.target.value;

	usernamesuccess.style.display='block';
	usernamesuccess.textContent="Checking"; 

	usernameField.classList.remove("is-invalid");
	feedbackArea.style.display="none";

	if(usernameVal.length>0){

		fetch("/validate-username/",{
		body: JSON.stringify({username:usernameVal}),
		method:"POST",
	})
		.then((res) => res.json())
		.then((data) => {
			console.log("data",data);
			usernamesuccess.style.display='none';
			if(data.username_error){
				usernameField.classList.add("is-invalid");
				feedbackArea.style.display="block";
				feedbackArea.innerHTML= data.username_error;

			}
		});

	}
	


});