

const showPassword=document.querySelector(".showPassword");
const passwordField=document.querySelector("#id_password");



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

