// una vez que todo haya cargado
var num_paginas = 0;
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

    num_paginas = 0;
   

});

function agregarPagina(){
    // obtiene la sección donde se van a guardar todos
    let seccion_paginas = document.getElementById("seccion_paginas");

    // crea div para elementos y lo pone en la sección
    let div_pagina = document.createElement('div');
    div_pagina.className = "mb-3";
    seccion_paginas.appendChild(div_pagina);

    // crea elementos, pone estilos, atributos
    let label_pagina = document.createElement('label') ;
    label_pagina.className = "form-label";
    label_pagina.innerHTML = "Texto";
    let textarea_pagina = document.createElement('textarea');
    textarea_pagina.setAttribute('name', 'texto_'+num_paginas);
    textarea_pagina.setAttribute('maxlength', '800');
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
}