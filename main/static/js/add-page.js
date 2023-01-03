// here are all javascript code for:
// dialogue, plain text, colors, etc.
var max_elem = 0;
$( document ).ready(function() {
    $("#add_dialog").click();

});

function destroy(id){
    $("#row_dialog_"+id).remove();
    let html = 
    `
    <div class="alert alert-success alert-dismissible fade show mb-2 mt-2" role="alert">
        <div style="text-align: center;">
            <strong>Elemento eliminado correctamente</strong>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `;
    document.getElementById("alert_removed_success").innerHTML = html;
}

function setFunctions(id){
    let content = document.getElementById("content_"+id);
    content.addEventListener("keyup", e => {
        content.style.height = content.style.fontSize;
        let h = e.target.scrollHeight;
        content.style.height = `${h}px`;
    });
    
    let translation = document.getElementById("translation_"+id);
    translation.addEventListener("keyup", e => {
        translation.style.height = content.style.fontSize;
        let h = e.target.scrollHeight;
        translation.style.height = `${h}px`;
    });

    $(".ch-color_"+id).css({'color':$("#color_"+id).val()});
    $("#color_"+id).on('input propertychange', (e)=>{
        $(".ch-color_"+id).css({'color':e.target.value});
    })
}

function addDialog(){
    let html = 
    `
    <div class="mb-3" id="row_dialog_`+max_elem+`" name="dialogs">
        <div class="row">
            <div class="col-12 col-md-3">
                <input class="form-control fs-5 fw-bold ch-color_`+max_elem+`" type="text" name="name" id="name_`+max_elem+`"
                    placeholder="Nombre" autocomplete="off">
                <div class="mt-2 d-flex">
                    <label for="color_`+max_elem+`" class="form-label me-2 fw-bold ch-color_`+max_elem+`">Color:</label>
                    <input class="form-control form-control-color mb-2 text-center shadow-none" type="color" name="color"
                        id="color_`+max_elem+`" value="#2DACFB">
                </div>
            </div>
            <div class="col-12 col-md-9">
                <textarea class="form-control fs-5 mb-2 txta" type="text" name="language1" id="content_`+max_elem+`"
                    placeholder="Contenido en inglés" maxlength="255"></textarea>
            </div>
        </div>
        <div class="row">
            <div class="col-12 col-md-10 mb-2">
                <textarea class="form-control fs-5 txta" type="text" name="language2" id="translation_`+max_elem+`"
                    placeholder="Contenido en español" maxlength="255"></textarea>
            </div>
            <div class="col-12 col-md-2 mb-2 text-center">
                <button class="btn btn-danger shadow-none" type="button" title="Eliminar diálogo"
                    data-bs-toggle="modal" data-bs-target="#modal_delete_`+max_elem+`">
                    <i class="fa-solid fa-trash"></i>
                </button>
                <div class="modal fade" id="modal_delete_`+max_elem+`" tabindex="-1"
                    aria-labelledby="exampleModalLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title  col-11 text-center">¿Desea eliminar este diálogo?</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="close"></button>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary"
                                    data-bs-dismiss="modal">Cancelar</button>
                                
                                <button class="btn btn-danger" type="button"
                                    onclick="destroy(`+max_elem+`)" data-bs-dismiss="modal">
                                    Eliminar</i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <input value="`+max_elem+`" name="element_number" hidden>
        <hr>
    </div>
    <div id="dialog_area"></div>
    `;

    document.getElementById("dialog_area").outerHTML = html;
    setFunctions(max_elem);
    max_elem++;
}