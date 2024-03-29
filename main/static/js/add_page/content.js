function addContent() {
	let selected = document.getElementById("content_selected").value;
	document.getElementById("content_area").outerHTML =
		`
    <span class="new_element"></span>
    <span id="content_area"></span>
		`;

	switch (parseInt(selected)) {
		case 0:
			addText();
			break;
		case 1:
			addDialogue();
			break;
	}
}


// Audio
function addAudio() {
	let string_id = generateStringId();
	document.querySelector(".new_element").outerHTML =
		`
		<div class="row exercise-sep" id="element_${max_elem}" name="audios">
			<div class="row">
        <div class="col-12 d-flex">
          <div class="col-10 col-md-11">
            <h3 class="fs-4 text-center my-3">Audio</h3>
          </div>
					${html_modal_delete(max_elem, '¿Desea eliminar este audio?')}
        </div>
      </div>

			<div class="col-12">
				<label class="form-label" for="audio_label_name_${max_elem}">
					Nombre del audio
					<span style="color:var(--f-orange);" title="Este elemento no se mostrará al estudiante">
						<i class="fa-solid fa-circle-question"></i>
					</span>
				</label>
				<input class="form-control mb-2" type="text" name="label_name" id="audio_label_name_${max_elem}"
					placeholder="Nombre del audio" maxlength="255">
			</div>

			<div class="col-12">
				<div class="row my-3">
					<div class="col-12">
						<div class="form-check form-switch">
							<input class="form-check-input" type="checkbox" name="show_description" 
								id="audio_add_description_${max_elem}"
								open="audio_add_description_container_${max_elem}"">
							<label class="form-check-label" for="audio_add_description_${max_elem}">Agregar descripción</label>
						</div>
					</div>
				</div>

				<div class="row mb-3 d-none" id="audio_add_description_container_${max_elem}" name="description_container">
					<div class="col-12">
						<div class="col-12">
							<label class="form-label" for="audio_description_${max_elem}">Descripción en inglés</label>
							<input class="form-control mb-2" type="text" 
								name="description" id="audio_description_${max_elem}"
								placeholder="Introduce un texto descriptivo en inglés" maxlength="600">
						</div>

						<div class="col-12">
							<label class="form-label" for="audio_t_description_${max_elem}">Descripción en español</label>
							<input class="form-control mb-2" type="text" 
								name="t_description" id="audio_t_description_${max_elem}"
								placeholder="Introduce un texto descriptivo en español" maxlength="600">
						</div>
					</div>
				</div>

			</div>

			<div class="col-12">
				<input type="file" id="file_${string_id}" name="audio_file" class="form-control" accept="audio/*">
				<input type="text" name="default_audio" readonly hidden>
			</div>

			<div class="col-12">
				<div style="display:flex; justify-content:center; width:100%; margin:1rem 0;">
					<audio controls name="audio_player" id="audio_player_${string_id}" controlsList="nodownload">
						<source src="" type="audio/mpeg">
					</audio>
				</div>
			</div>
			<input value="${max_elem}" name="element_number" hidden>
			<input name="id" hidden>
		</div>
	`;

	document.getElementById(`audio_add_description_${max_elem}`).addEventListener('change', (e) => {
		let container = document.getElementById(e.target.getAttribute('open'));
		if (e.target.checked)
			container.classList.remove('d-none');
		else
			container.classList.add('d-none');
	});

	document.getElementById('file_' + string_id).addEventListener('change', (e) => {
		let audio_player_id = e.target.id.replace('file_', 'audio_player_');
		let audio_player = document.getElementById(audio_player_id);
		audio_player.volume = 0.5;

		const file = e.target.files[0];

		if (file != undefined) {
			audio_player.src = URL.createObjectURL(file);;
		}
		else {
			let default_audio = e.target.parentElement.querySelector('[name = default_audio]').value;
			if (default_audio != '') {
				// get the audio as blob
				fetch(default_audio)
					.then(response => response.blob())
					.then(blob => {
						audio_player.src = URL.createObjectURL(blob);
					})
					.catch(error => {
						console.error('Error fetching the audio file:', error);
					});
			}
			else
				audio_player.src = "";
		}

	});

	max_elem++;
}


// Image
function addImage() {
	let string_id = generateStringId();
	document.querySelector(".new_element").outerHTML =
		`
		<div class="row exercise-sep" id="element_${max_elem}" name="images">
			<div class="row">
        <div class="col-12 d-flex">
          <div class="col-10 col-md-11">
            <h3 class="fs-4 text-center my-3">Imagen</h3>
          </div>
					${html_modal_delete(max_elem, '¿Desea eliminar esta imagen?')}
        </div>
      </div>

			<div class="col-12">
				<div style="display:flex; justify-content:center; width:100%; margin:1rem 0;">
					<img class="box-shadow d-none" alt="No se pudo cargar la imagen" name="preview" id="preview_${string_id}"
					style="max-height:450px; max-width:100%;">
				</div>
			</div>
			<div class="col-12">
				<input type="file" id="file_${string_id}" name="image_file" class="form-control" accept="image/*">
				<input type="text" name="default_image" readonly hidden>
			</div>
			<input value="${max_elem}" name="element_number" hidden>
			<input name="id" hidden>
		</div>
	`;

	document.getElementById('file_' + string_id).addEventListener('change', (e) => {
		let preview_id = e.target.id.replace('file_', 'preview_');
		let preview_image = document.getElementById(preview_id);

		if (e.target.value == "") {
			let default_image = e.target.parentElement.querySelector('[name = default_image]').value;

			preview_image.setAttribute('src', default_image);

			if (default_image == '')
				preview_image.classList.add('d-none');
			else
				preview_image.classList.remove('d-none');
		}

		if (e.target.files && e.target.files[0]) {
			let reader = new FileReader();
			reader.onload = function (r) {
				preview_image.setAttribute('src', r.target.result);
				preview_image.classList.remove('d-none');
			};
			reader.readAsDataURL(e.target.files[0]);
		}
	});

	max_elem++;
}

// Video
function addVideo(include_delete_button) {
	let delete_row =
		`
		<div class="row">
			<div class="col-12 d-flex">
				<div class="col-10 col-md-11">
					<h3 class="fs-4 text-center my-3">Video</h3>
				</div>
				${html_modal_delete(max_elem, '¿Desea eliminar este video?')}
			</div>
		</div>
		`;

	if (include_delete_button !== undefined)
		if (!include_delete_button)
			delete_row = ''

	document.querySelector(".new_element").outerHTML =
		`
		<div class="row exercise-sep" id="element_${max_elem}" name="videos">
			${delete_row}
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
		`;
	max_elem++;
}

// Text
function addText() {
	document.querySelector(".new_element").outerHTML =
		`
		<div class="row exercise-sep" id="element_`+ max_elem + `" name="texts">

			<div class="row">
        <div class="col-12 d-flex">
          <div class="col-10 col-md-11">
            <h3 class="fs-4 text-center my-3">Texto</h3>
          </div>
					${html_modal_delete(max_elem, '¿Desea eliminar este texto?')}
        </div>
      </div>

			<div class="col-12">
				<label class="form-label" for="text_content1_${max_elem}">Texto en inglés</label>
				<textarea class="form-control mb-2 txta" type="text" name="language1" id="text_content1_${max_elem}"
					placeholder="Texto en inglés"></textarea>
			</div>
			<div class="col-12">
			<label class="form-label" for="text_content2_${max_elem}">Texto en español</label>
				<textarea class="form-control mb-2 txta" type="text" name="language2" id="text_content2_${max_elem}"
					placeholder="Texto en español"></textarea>
			</div>

			<input value="`+ max_elem + `" name="element_number" hidden>
			<input name="id" hidden>
		</div>
		`;

	let adj1 = document.getElementById("text_content1_" + max_elem);
	let adj2 = document.getElementById("text_content2_" + max_elem);
	makeAdjustable(adj1);
	makeAdjustable(adj2);
	max_elem++;
}


function addDialogue() {
	document.querySelector(".new_element").outerHTML =
		`
		<div class="exercise-sep" id="element_`+ max_elem + `" name="dialogues">
			
			<div class="row">
				<div class="col-12 d-flex">
					<div class="col-10 col-md-11">
						<h3 class="fs-4 text-center my-3">Diálogo</h3>
					</div>
					${html_modal_delete(max_elem, '¿Desea eliminar este diálogo?')}
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
		`;

	let adj1 = document.getElementById("language1_" + max_elem);
	let adj2 = document.getElementById("language2_" + max_elem);
	makeAdjustable(adj1);
	makeAdjustable(adj2);

	setFunctions(max_elem);
	max_elem++;
}


/* More functions */
// Image
function restoreImage() {
	$("#img_showed").attr("src", default_cover);
	$("#image").val("");
}

function changeImg(input) {
	if (input.value == "")
		restoreImage();
	if (input.files && input.files[0]) {
		let reader = new FileReader();
		reader.onload = function (e) {
			$("#img_showed").attr("src", e.target.result);
		};
		reader.readAsDataURL(input.files[0]);
	}
}

// Dialog
function setFunctions(id) {
	$(".ch-color_" + id).css({ 'color': $("#color_" + id).val() });
	$("#color_" + id).on('input propertychange', (e) => {
		$(".ch-color_" + id).css({ 'color': e.target.value });
	});
}

// Video
function verifyVideo(element_number) {
	element = document.getElementById('element_' + element_number);

	url = element.querySelector('[name = url]').value;
	video_showed_container = element.querySelector('.video-showed');
	video = video_showed_container.children[0];

	valid_url = validateUrl(url);
	if (valid_url !== "") {
		video.src = valid_url;
		video_showed_container.classList.remove("d-none");
	}
	else
		video_showed_container.classList.add("d-none");
}

function validateUrl(url) {
	if (url.startsWith("https://www.youtube.com/embed/"))
		return url;
	if (url.startsWith("https://www.youtube.com/watch?v=")) {
		code = url.split("https://www.youtube.com/watch?v=")[1];
		return "https://www.youtube.com/embed/" + code;
	}
	if (url.startsWith("https://youtu.be/")) {
		code = url.split("https://youtu.be/")[1];
		return "https://www.youtube.com/embed/" + code;
	}
	return "";
}