function addExercise() {
  let selected = document.getElementById("exercise_selected").value;
  document.getElementById("exercises_area").outerHTML =
    `
    <span class="new_element"></span>
    <span id="exercises_area"></span>
  `;

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
  document.querySelector(".new_element").outerHTML =
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
  `;



  let adj1 = document.getElementById("repP1_" + max_elem);
  let adj2 = document.getElementById("repP2_" + max_elem);
  makeAdjustable(adj1);
  makeAdjustable(adj2);

  max_elem++;
}


function addSpellcheck() {
  document.querySelector(".new_element").outerHTML =
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
      <div class="row">
        <div class="col-12 col-sm-6 mb-2">
          <label class="form-label" for="rspc_`+ max_elem + `">Texto en inglés</label>
          <textarea class="form-control mb-2 txta" type="text" name="right_text" id="rspc_`+ max_elem + `"
            placeholder="Texto en inglés"></textarea>
        </div>

        <div class="col-12 col-sm-6 mb-2">
          <label class="form-label" for="trspc_`+ max_elem + `">Texto en español</label>
          <textarea class="form-control mb-2 txta" type="text" name="translated_right_text" id="trspc_`+ max_elem + `"
            placeholder="Texto en español"></textarea>
        </div>
      </div>

      <div class="col-12">
        <label class="form-label" for="wspc_`+ max_elem + `">Texto en inglés (con errores)</label>
				<textarea class="form-control mb-2 txta" type="text" name="wrong_text" id="wspc_`+ max_elem + `"
					placeholder="Texto en inglés (con errores)"></textarea>
			</div>

      <input value="`+ max_elem + `" name="element_number" hidden>
      <input name="id" hidden>
    </div>
  `;

  let adj1 = document.getElementById("wspc_" + max_elem);
  let adj2 = document.getElementById("rspc_" + max_elem);
  let adj3 = document.getElementById("trspc_" + max_elem);
  makeAdjustable(adj1);
  makeAdjustable(adj2);
  makeAdjustable(adj3);

  max_elem++;
}

function html_modal_delete(max_elem, message, cols) {
  if (cols === undefined) {
    cols = "col-2 col-md-1";//d-flex align-items-center
  }
  let html =
    `
  <div class="${cols}" style="display:flex; align-items:center; justify-content:center;">
    <button class="btn btn-danger shadow-none" type="button" title="Eliminar elemento" data-bs-toggle="modal"
      data-bs-target="#modal_delete_${max_elem}">
      <i class="fa-solid fa-trash"></i>
    </button>
    <div class="modal fade" id="modal_delete_${max_elem}" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title  col-11 text-center">${message}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="close"></button>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
            <button type="button" class="btn btn-danger" onclick="deleteElement('${max_elem}')" data-bs-dismiss="modal">
              Eliminar</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  `;
  return html;
}

function addMultipleChoiceQuestion() {
  let mcq_id = generateStringId();
  let choices_id = "choices_" + mcq_id;
  let add_choice_id = "add_choice_" + mcq_id;

  document.querySelector(".new_element").outerHTML =
    `
  <div class="row exercise-sep" id="element_${max_elem}" name="mc_questions">
    <input name="id" hidden>
    <input name="element_number" value="${max_elem}" hidden>
    <input type="number" name="choices_number" value="0" hidden>
    <div class="row">
      <div class="col-12 d-flex">
        <div class="col-10 col-md-11">
          <h3 class="fs-4 text-center my-3 title">Pregunta de opción múltiple</h3>
        </div>
        ${html_modal_delete(max_elem, '¿Desea eliminar esta pregunta?')}
      </div>
    </div>

    <div class="row">
      <div class="col-12 col-sm-6 mb-2">
        <label class="form-label" for="mcqt_${max_elem}">Pregunta en inglés</label>
        <textarea class="form-control txta" type="text" id="mcqt_${max_elem}" name="text"
          placeholder="Pregunta en inglés" maxlength="255"></textarea>
      </div>

      <div class="col-12 col-sm-6 mb-2">
        <label class="form-label" for="mcqtt_${max_elem}">Pregunta en español</label>
        <textarea class="form-control txta" type="text" id="mcqtt_${max_elem}" name="t_text"
          placeholder="Pregunta en español" maxlength="255"></textarea>
      </div>
    </div>

    <div class="col-12 mb-2 text-center">
      <div class="form-check  d-inline-block">
        <input type="checkbox" class="form-check-input" name="randomize_choices" id="mcqr_${max_elem}" checked>
        <label class="form-label" for="mcqr_${max_elem}">Mostrar opciones aleatoriamente</label>
      </div>
    </div>

    <div class="col-12 mb-2 text-center">
      <h3 class="fs-5 title fst-italic" style="color: #606060;">Opciones</h3>
      <ul class="question-choices">
        <li id="${choices_id}"></li>
      </ul>
      <div class="row my-3">
        <div class="add-choice-button" id="${add_choice_id}">
          <span class=""><i class="fa-solid fa-plus"></i></span>
          Agregar opción
        </div>
      </div>
    </div>

    
  </div>
  `;

  makeAdjustable(document.getElementById("mcqt_" + max_elem));
  makeAdjustable(document.getElementById("mcqtt_" + max_elem));
  let choices_input = document.querySelector(`#element_${max_elem} input[name=choices_number]`);
  document.getElementById(add_choice_id).addEventListener('click', (e) => {
    addQuestionChoice(choices_id, choices_input.value);
    choices_input.value = parseInt(choices_input.value) + 1;
  });
  max_elem++;
  let util = {
    "add_choice_id": add_choice_id
  }
  return util;
}

function addQuestionChoice(choices_id, choice_number) {
  let question_choice_id = "choice_" + generateStringId();
  document.getElementById(choices_id).outerHTML =
    `
  <li id="element_${question_choice_id}" class="choice" name="question_choices">
    <input name="id" hidden>
    <input type="number" name="choice_number" value="${choice_number}" hidden>
    
    <div class="row choice-container" name="correct">
      <div class="col-12 col-sm-1 radio-container">
        <div class="radio-btn choice_name_${choices_id}" id="radio_label_${question_choice_id}">
          <i class="fa-solid fa-check"></i>
        </div>
      </div>
      <div class="d-inline-block mb-3 d-sm-none"></div>

      <div class="col-12 col-sm-5">
        <div class="mb-3">
          <label for="${question_choice_id}_t_text" class="form-label">Opción en inglés</label>
          <input name="text" type="text" class="form-control" placeholder="Opción en inglés"
          id="${question_choice_id}_t_text" autocomplete="off" maxlength="255">
        </div>
      </div>

      <div class="col-12 col-sm-5">
        <div class="mb-3">
          <label for="${question_choice_id}_text" class="form-label">Opción en español</label>
          <input name="t_text" type="text" class="form-control" placeholder="Opción en español" 
          id="${question_choice_id}_text" autocomplete="off" maxlength="255">
        </div>
      </div>

      ${html_modal_delete(question_choice_id, '¿Estás seguro de eliminar esta opción?', 'col-12 col-sm-1')}
    </div>
  </li>
  <li id="${choices_id}"></li>
  `;

  let current_radio = document.getElementById('radio_label_' + question_choice_id);
  current_radio.addEventListener('click', (e) => {
    let radios = document.getElementsByClassName('choice_name_' + choices_id);
    for (let r of radios) {
      r.classList.remove('selected');
      // Main row
      r.parentElement.parentElement.classList.remove('checked');
    }
    current_radio.classList.add('selected');
    // Main row
    current_radio.parentElement.parentElement.classList.add('checked');
  });
}