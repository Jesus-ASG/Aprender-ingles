document.addEventListener("DOMContentLoaded", function () {
    // cambiar clase de contenedor
    var cambiar = document.querySelector("#id_id_categoria").childNodes;
    for (var i = 0; i < cambiar.length; i++)
        cambiar[i].className = "form-check form-check-inline";

    // cambiar clase de checkbox
    for (var i = 0; i < cambiar.length; i++)
        document.getElementById("id_id_categoria_" + i).className = "form-check-input";

});