// una vez que todo haya cargado
document.addEventListener("DOMContentLoaded", function () {
    // categorias
    // cambiar clase de contenedor
    var cambiar = document.querySelector("#id_id_categoria").childNodes;
    for (var i = 0; i < cambiar.length; i++)
        cambiar[i].className = "form-check form-check-inline";

    // cambiar clase de checkbox
    var checks = document.getElementsByName("id_categoria");
    for (var i = 0; i < checks.length; i++)
        checks[i].className = "form-check-input";
    // --------------------- ////

    // Paginas
    /*
    var arr_paginas = document.getElementsByClassName("txt-historias");
    for (var i = 0; i < 1; i++){
        arr_paginas[i].addEventListener("keyup", e => {
            arr_paginas[i].style.height = "60px";
            let scHeight = e.target.scrollHeight;
            arr_paginas[i].style.height = `${scHeight}px`;
        });
    }*/
    

    var arr_paginas = document.getElementsByClassName("txt-historias");
    //var txt = document.getElementById("id_texto");
    //console.log(txt);
    arr_paginas[0].addEventListener("keyup", e => {
        arr_paginas[0].style.height = "60px";
        let scHeight = e.target.scrollHeight;
        arr_paginas[0].style.height = `${scHeight}px`;
    });
   

});