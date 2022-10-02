//Comprobar igualdad de las contraseñas
var pass1 = document.getElementById("password1");
var pass2 = document.getElementById("password2");
var btn_registrarse = document.getElementById("btn_registrarse");

msg_pass = document.getElementById("mensajes_pass");

pass1.addEventListener("keyup", e => {
    msg_pass.hidden = false;

    var b1 = matchPass();
    var b2 = numYLetra();
    var b3 = funLongitud();
    var b4 = funNo12345678();

    if (b1 && b2 && b3 && b4)
        btn_registrarse.disabled = false;
    else
        btn_registrarse.disabled = true;
    
});
pass2.addEventListener("keyup", e => {
    msg_pass.hidden = false;
    var b1 = matchPass();
    var b2 = numYLetra();
    var b3 = funLongitud();
    var b4 = funNo12345678();

    if (b1 && b2 && b3 && b4)
        btn_registrarse.disabled = false;
    else
        btn_registrarse.disabled = true;
});


function matchPass(){
    pass1 = document.getElementById("password1").value;
    pass2 = document.getElementById("password2").value;
    // las contraseñas coinciden
    if (pass1 == pass2 && pass1!="" && pass2!=""){
        document.getElementById("match").className = "";
        return true;
    }
    else{
        document.getElementById("match").className = "error-pass";
        return false;
    }
}

function numYLetra(){
    pass2 = document.getElementById("password2").value;
    pass1 = document.getElementById("password1").value;
    var letras = /[a-zA-Z]/g;
    var numeros = /[0-9]/g;
    if(letras.test(pass2) && numeros.test(pass2) ){
        document.getElementById("num_y_letra").className = "";
        return true;
    }
    else{
        document.getElementById("num_y_letra").className = "error-pass";
        return false;
    }
}

function funLongitud(){
    pass2 = document.getElementById("password2").value;
    pass1 = document.getElementById("password1").value;
    if (pass2.length >= 8 ){
        document.getElementById("longitud").className = "";
        return true;
    }
    else{
        document.getElementById("longitud").className = "error-pass";
        return false;
    }
}

function funNo12345678(){
    pass2 = document.getElementById("password2").value;
    pass1 = document.getElementById("password1").value;
    if(pass2 != "12345678" ){
        document.getElementById("no12345678").className = "";
        return true;
    }
    else{
        document.getElementById("no12345678").className = "error-pass";
        return false;
    }
}


// mostrar / ocultar contraseñas
btn_eye1 = document.getElementById("btn_eye1");
btn_eye2 = document.getElementById("btn_eye2");

btn_eye1.addEventListener("click", e => {
    eye_1 = document.getElementById("eye_1");
    if(eye_1.classList.contains("fa-eye-slash")){        
        eye_1.className = "fa-solid fa-eye";
        document.getElementById("password1").type = "text";
    }
    else{
        eye_1.className = "fa fa-eye-slash";
        document.getElementById("password1").type = "password"; 
    }
});

btn_eye2.addEventListener("click", e => {
    eye_2 = document.getElementById("eye_2");
    if(eye_2.classList.contains("fa-eye-slash")){        
        eye_2.className = "fa-solid fa-eye";
        document.getElementById("password2").type = "text";
    }
    else{
        eye_2.className = "fa fa-eye-slash";
        document.getElementById("password2").type = "password"; 
    }
});