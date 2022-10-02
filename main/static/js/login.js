btn_eye1 = document.getElementById("btn_eye1");

btn_eye1.addEventListener("click", e => {
    eye_1 = document.getElementById("eye_1");
    if(eye_1.classList.contains("fa-eye-slash")){        
        eye_1.className = "fa-solid fa-eye";
        document.getElementById("password").type = "text";
    }
    else{
        eye_1.className = "fa fa-eye-slash";
        document.getElementById("password").type = "password"; 
    }
});