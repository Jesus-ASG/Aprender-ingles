function addContent() {
	let selected = document.getElementById("content_selected").value;
	switch (parseInt(selected)) {
		case 0:
			addText();
			break;
		case 1:
			addDialogue();
			break;

		default:
		//console.log("nothing");
	}
}

// Video
function addVideo() {
	document.getElementById("content_area").outerHTML =
		`
		<div class="row exercise-sep" id="element_${max_elem}" name="videos">
			<div class="row mb-3">
				<div class="col-12">
					<label class="form-label fs-5" for="video_url_input_${max_elem}">Agrega un video de
						<a href="https://www.youtube.com" target="_blank" class="external-link" title="Ir a Youtube">
							YouTube <span><i class="fa-solid fa-arrow-up-right-from-square" style="font-size: 1rem;"></i></span>
						</a>
					</label>
				</div>
				<div class="col-12 col-md-8">
					<input class="text-center form-control" id="video_url_input_${max_elem}" name="url"
					placeholder="Url del video" autocomplete="false">
					<input value="${max_elem}" name="element_number" hidden>
					<input name="id" hidden>
				</div>
				<div class="col-12 col-md-4">
					<button class="btn btn-primary w-100" onclick="verifyVideo(${max_elem})">Verificar video</button>
				</div>
				<div id="video_url_display_c_${max_elem}" class="video-showed d-none">
					<iframe class="video-frame" title="YouTube video player" frameborder="0"
						allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
						allowfullscreen></iframe>
				</div>
			</div>
    </div>
		<div id="content_area"></div>
	`;
	max_elem++;
}

// Text
function addText() {
	document.getElementById("content_area").outerHTML =
		`
		<div class="row exercise-sep" id="element_`+ max_elem + `" name="texts">
			
			<div class="row">
        <div class="col-12 d-flex">
          <div class="col-10 col-md-11">
            <h3 class="fs-4 text-center my-3">Texto</h3>
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
                    <h5 class="modal-title  col-11 text-center">¿Desea eliminar este texto?</h5>
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
				<textarea class="form-control mb-2 txta" type="text" name="language1" id="text_content1_`+ max_elem + `"
					placeholder="Contenido en inglés"></textarea>
			</div>
			<div class="col-12">
				<textarea class="form-control mb-2 txta" type="text" name="language2" id="text_content2_`+ max_elem + `"
					placeholder="Contenido en español"></textarea>
			</div>

			<input value="`+ max_elem + `" name="element_number" hidden>
			<input name="id" hidden>
		</div>
		<div id="content_area"></div>
	`;
	let adj1 = document.getElementById("text_content1_" + max_elem);
	let adj2 = document.getElementById("text_content2_" + max_elem);
	makeAdjustable(adj1);
	makeAdjustable(adj2);
	max_elem++;
}


// Dialog
function setFunctions(id) {
	$(".ch-color_" + id).css({ 'color': $("#color_" + id).val() });
	$("#color_" + id).on('input propertychange', (e) => {
		$(".ch-color_" + id).css({ 'color': e.target.value });
	});
}

function addDialogue() {
	document.getElementById("content_area").outerHTML =
		`
	
	<div class="exercise-sep" id="element_`+ max_elem + `" name="dialogues">
		
		<div class="row">
			<div class="col-12 d-flex">
				<div class="col-10 col-md-11">
					<h3 class="fs-4 text-center my-3">Diálogo</h3>
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
									<h5 class="modal-title  col-11 text-center">¿Desea eliminar este diálogo?</h5>
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
			<div class="col-12 col-md-3">
				<input class="form-control fw-bold ch-color_`+ max_elem + `" type="text" name="name" id="name_` + max_elem + `"
					placeholder="Nombre" autocomplete="off">
				<div class="mt-2 d-flex">
					<label for="color_`+ max_elem + `" class="form-label me-2 fw-bold ch-color_` + max_elem + `">Color:</label>
					<input class="form-control form-control-color mb-2 text-center shadow-none" type="color" name="color"
						id="color_`+ max_elem + `" value="#2DACFB">
				</div>
			</div>
			<div class="col-12 col-md-9">
				<textarea class="form-control mb-2 txta" type="text" name="language1" id="language1_`+ max_elem + `"
					placeholder="Contenido en inglés" maxlength="255"></textarea>
			</div>
		</div>
		<div class="row">
			<div class="col-12 mb-2">
				<textarea class="form-control txta" type="text" name="language2" id="language2_`+ max_elem + `"
					placeholder="Contenido en español" maxlength="255"></textarea>
			</div>
		</div>
		<input value="`+ max_elem + `" name="element_number" hidden>
		<input name="id" hidden>
		
	</div>
	
	<div id="content_area"></div>
  `;

	let adj1 = document.getElementById("language1_" + max_elem);
	let adj2 = document.getElementById("language2_" + max_elem);
	makeAdjustable(adj1);
	makeAdjustable(adj2);

	setFunctions(max_elem);
	max_elem++;
}