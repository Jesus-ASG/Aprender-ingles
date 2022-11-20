// here are all javascript code for:
// dialogue, plain text, colors, etc.
var num_d = 1;
$( document ).ready(function() {
    
    let content = document.getElementById("content");
    content.addEventListener("keyup", e => {
        content.style.height = content.style.fontSize;
        let h = e.target.scrollHeight;
        content.style.height = `${h}px`;
    });
    
    let translation = document.getElementById("translation");
    translation.addEventListener("keyup", e => {
        translation.style.height = content.style.fontSize;
        let h = e.target.scrollHeight;
        translation.style.height = `${h}px`;
    });

    $(".ch-color").css({'color':$("#color").val()});
    $("#color").change(function(){
        $(".ch-color").css({'color':$("#color").val()});
    });

});

function setIncreaseHeight(){
    
}


function addDialog(){
    num_d++;


    
    /*
    let dialog_area = document.getElementById("dialog_area");

    let container = document.createElement('div');
    container.className = "mb-3";
    seccion_paginas.appendChild(div_pagina);

    // crea elementos, pone estilos, atributos
    let label_pagina = document.createElement('label') ;
    label_pagina.className = "form-label";
    label_pagina.innerHTML = "Texto";
    let textarea_pagina = document.createElement('textarea');
    textarea_pagina.setAttribute('name', 'texto_'+num_paginas);
    textarea_pagina.setAttribute('maxlength', '255');
    textarea_pagina.setAttribute('id', 'texto_'+num_paginas);
    textarea_pagina.classList.add("txt-historias");
    textarea_pagina.classList.add("form-control");

    textarea_pagina.addEventListener("keyup", e => {
        textarea_pagina.style.height = "60px";
        let scHeight = e.target.scrollHeight;
        textarea_pagina.style.height = `${scHeight}px`;
    });

    // agrega elementos al div
    div_pagina.appendChild(label_pagina);
    div_pagina.appendChild(textarea_pagina);
    // focus al textarea
    textarea_pagina.focus();
    
    // incrementa el contador de páginas
    num_paginas++;
    document.getElementById("num_paginas").value = num_paginas;
    */
}