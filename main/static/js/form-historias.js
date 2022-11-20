// change styles showing categories
document.addEventListener("DOMContentLoaded", function () {
    // categorias
    // cambiar clase de contenedor
    var cambiar = document.querySelector("#id_tag").childNodes;
    for (let i = 0; i < cambiar.length; i++)
        cambiar[i].className = "form-check form-check-inline";

    // cambiar clase de checkbox
    var checks = document.getElementsByName("tag");
    for (let i = 0; i < checks.length; i++)
        checks[i].className = "form-check-input";
    // --------------------- ////

});