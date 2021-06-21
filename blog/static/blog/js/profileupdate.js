
const usernameField=document.querySelector("#id_username");
const feedbackArea=document.querySelector(".invalid-feedback");


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