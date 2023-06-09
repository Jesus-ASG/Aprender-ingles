function addExercise() {
  let selected = document.getElementById("exercise_selected").value;
  switch (parseInt(selected)) {
    case 0:
      repeatPhrase();
      break;
    case 1:
      addSpellcheck();
      break;
    case 2:
      addMultipleChoiceQuestion();
      break;

    default:
    //console.log("nothing");
  }
}

function repeatPhrase() {
  let html =
    `
    <div class="exercise-sep" id="element_`+ max_elem + `" name="repeatPhrases">
      
      <div class="row">
        <div class="col-12 d-flex">
          <div class="col-10 col-md-11">
            <h3 class="fs-4 text-center my-3">Repetir oración</h3>
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
        <div class="col-12 mb-2">
        <label class="form-label" for="repP1_`+ max_elem + `">Escribe el contenido en inglés</label>
          <textarea class="form-control txta" type="text" id="repP1_`+ max_elem + `" name="language1" placeholder="Contenido en inglés"
            maxlength="255"></textarea>
        </div>
      </div>
      <div class="row">
        <div class="col-12 mb-2">
        <label class="form-label" for="repP2_`+ max_elem + `">Escribe el contenido en español</label>
          <textarea class="form-control txta" type="text" id="repP2_`+ max_elem + `" name="language2"
            placeholder="Contenido en español" maxlength="255"></textarea>
        </div>
      </div>
      <div class="row"> 
        <div class="col-12 mb-2 text-center">
          <div class="form-check  d-inline-block">
            <input type="checkbox" class="form-check-input fs-5" name="show_text" id="show_text_`+ max_elem + `"
            placeholder="Contenido en español" maxlength="255" checked>
            <label class="form-label fs-5" for="show_text_`+ max_elem + `">Mostrar texto</label>
          </div>
        </div>
      </div>
      <input value="`+ max_elem + `" name="element_number" hidden>
      <input name="id" hidden>
      
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


function addSpellcheck() {
  document.getElementById("exercises_area").outerHTML =
    `
    <div class="exercise-sep" id="element_`+ max_elem + `" name="spellchecks">
      <div class="row">
        <div class="col-12 d-flex">
          <div class="col-10 col-md-11">
            <h3 class="fs-4 text-center my-3">Revisar ortografía</h3>
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
      <div class="col-12">
        <label class="form-label" for="wspc_`+ max_elem + `">Texto con errores</label>
				<textarea class="form-control mb-2 txta" type="text" name="wrong_text" id="wspc_`+ max_elem + `"
					placeholder="Texto con errores"></textarea>
			</div>

      <div class="col-12">
        <label class="form-label" for="rspc_`+ max_elem + `">Texto sin errores</label>
				<textarea class="form-control mb-2 txta" type="text" name="right_text" id="rspc_`+ max_elem + `"
					placeholder="Texto sin errores"></textarea>
			</div>

      <div class="col-12">
        <label class="form-label" for="trspc_`+ max_elem + `">Texto traducido sin errores</label>
				<textarea class="form-control mb-2 txta" type="text" name="translated_right_text" id="trspc_`+ max_elem + `"
					placeholder="Texto traducido sin errores"></textarea>
			</div>
      <input value="`+ max_elem + `" name="element_number" hidden>
      <input name="id" hidden>
    </div>
    <span id="exercises_area"></span>
  `;

  let adj1 = document.getElementById("wspc_" + max_elem);
  let adj2 = document.getElementById("rspc_" + max_elem);
  let adj3 = document.getElementById("trspc_" + max_elem);
  makeAdjustable(adj1);
  makeAdjustable(adj2);
  makeAdjustable(adj3);

  max_elem++;
}

function addMultipleChoiceQuestion() {
  document.getElementById("exercises_area").outerHTML =
    `
    <div class="exercise-sep" id="element_`+ max_elem + `" name="questions">
      <div class="row">
        <div class="col-12 d-flex">
          <div class="col-10 col-md-11">
            <h3 class="fs-4 text-center my-3">Revisar ortografía</h3>
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
      <div class="col-12">
        <label class="form-label" for="wspc_`+ max_elem + `">Texto con errores</label>
				<textarea class="form-control mb-2 txta" type="text" name="wrong_text" id="wspc_`+ max_elem + `"
					placeholder="Texto con errores"></textarea>
			</div>

      <div class="col-12">
        <label class="form-label" for="rspc_`+ max_elem + `">Texto sin errores</label>
				<textarea class="form-control mb-2 txta" type="text" name="right_text" id="rspc_`+ max_elem + `"
					placeholder="Texto sin errores"></textarea>
			</div>

      <div class="col-12">
        <label class="form-label" for="trspc_`+ max_elem + `">Texto traducido sin errores</label>
				<textarea class="form-control mb-2 txta" type="text" name="translated_right_text" id="trspc_`+ max_elem + `"
					placeholder="Texto traducido sin errores"></textarea>
			</div>
      <input value="`+ max_elem + `" name="element_number" hidden>
      <input name="id" hidden>
    </div>
    <span id="exercises_area"></span>
  `;


  max_elem++;
}
