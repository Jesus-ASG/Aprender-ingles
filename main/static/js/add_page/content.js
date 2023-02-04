// Dialog
function setFunctions(id){
	$(".ch-color_"+id).css({'color':$("#color_"+id).val()});
	$("#color_"+id).on('input propertychange', (e)=>{
		$(".ch-color_"+id).css({'color':e.target.value});
	});
}

function addDialogue(){
  let html = 
  `
	<div class="mb-3" id="element_`+max_elem+`" name="dialogues">
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
				<textarea class="form-control fs-5 mb-2 txta" type="text" name="language1" id="language1_`+max_elem+`"
					placeholder="Contenido en inglés" maxlength="255"></textarea>
			</div>
		</div>
		<div class="row">
			<div class="col-12 col-md-10 mb-2">
				<textarea class="form-control fs-5 txta" type="text" name="language2" id="language2_`+max_elem+`"
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
									onclick="deleteElement(`+max_elem+`)" data-bs-dismiss="modal">
									Eliminar</i>
								</button>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<input value="`+max_elem+`" name="element_number" hidden>
		<input name="id" hidden>
		<hr>
	</div>
	<div id="content_area"></div>
  `;

  document.getElementById("content_area").outerHTML = html;

  let adj1 = document.getElementById("language1_" + max_elem);
  let adj2 = document.getElementById("language2_" + max_elem);
  makeAdjustable(adj1);
  makeAdjustable(adj2);

  setFunctions(max_elem);
  max_elem++;
}