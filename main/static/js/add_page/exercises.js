function addExercise() {
  let selected = document.getElementById("exercise_selected").value;
  switch (parseInt(selected)) {
    case 0:
      repeatPhrase();
      break;

    default:
    //console.log("nothing");
  }
}

function repeatPhrase() {
  let html =
    `
    <div class="mb-3" id="element_`+ max_elem + `" name="repeatPhrases">
      <hr>
      <div class="row">
        <div class="col-12 d-flex">
          <div class="col-10 col-md-11">
            <h3 class="fs-3 text-center my-3">Repetir oración</h3>
          </div>
          <div class="col-2 col-md-1 d-flex align-items-center">
            <button class="btn btn-danger shadow-none" type="button" title="Eliminar elemento" data-bs-toggle="modal"
            data-bs-target="#modal_delete_`+ max_elem + `">
              <i class="fa-solid fa-trash"></i>
            </button>
            <div class="modal fade" id="modal_delete_`+ max_elem + `" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
              <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
                <div class="modal-content">
                  <div class="modal-header">
                    <h5 class="modal-title  col-11 text-center">¿Desea eliminar este ejercicio?</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="close"></button>
                  </div>
                  <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="button" class="btn btn-danger" onclick="deleteElement(`+ max_elem + `)" data-bs-dismiss="modal">
                    Eliminar</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <label class="form-label fs-5" for="repl">Escribe el contenido en inglés</label>
        <div class="col-12 mb-2">
          <textarea class="form-control fs-5 txta" type="text" id="repP1_`+ max_elem + `" name="language1" placeholder="Contenido en inglés"
            maxlength="255"></textarea>
        </div>
      </div>
      <div class="row">
        <label class="form-label fs-5" for="repl1">Escribe el contenido en español</label>
        <div class="col-12 mb-2">
          <textarea class="form-control fs-5 txta" type="text" id="repP2_`+ max_elem + `" name="language2"
            placeholder="Contenido en español" maxlength="255"></textarea>
        </div>
      </div>
      <input value="`+max_elem+`" name="element_number" hidden>
      <input name="id" hidden>
      <hr>
    </div>
    <span id="exercises_area"></span>
  `;

  document.getElementById("exercises_area").outerHTML = html;

  let adj1 = document.getElementById("repP1_" + max_elem);
  let adj2 = document.getElementById("repP2_" + max_elem);
  makeAdjustable(adj1);
  makeAdjustable(adj2);

  max_elem++;
}