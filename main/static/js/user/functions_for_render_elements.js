// Contents
function renderDialogue(dialogue, total_translations) {
	let html_dialogue = ``;
	let text1 = dialogue.content1.replace(/\n/g, '<span></span>|');
	let text2 = dialogue.content2.replace(/\n/g, '<span></span>|');

	let flipClasses = {
		"paper": "fs-5 mx-1",
		"front": "px-1",
		"back": "px-1"
	};
	html_dialogue += `
	<div class="row" style="color:rgba(0,0,0,0)"><br></div>
	<div class="fw-bold fs-5 dialogue-name" style="color:`+ dialogue.color + `;">
		<p>`+ dialogue.name + `:</p>
	</div>
	`+ createFlipHTML(text1, text2, total_translations, flipClasses) + `
	<div id="content_area"></div>`;

	document.getElementById("content_area").outerHTML = html_dialogue;
}

// Exercises
function renderRepeatPhrase(repeat_phrase, total_translations) {
	let html_repeat_phrase = ``;
	let text1 = repeat_phrase.content1.replace(/\n/g, '<span></span>|').trim();
	let text2 = repeat_phrase.content2.replace(/\n/g, '<span></span>|').trim();
	let flipClasses = {
		"paper": "mx-1 fw-bold fst-italic text-dark",
		"front": "px-1",
		"back": "px-1"
	};
	let text_to_repeat = '';
	if (repeat_phrase.show_text)
		text_to_repeat = createFlipHTML(`Repeat: "`+text1+`"`, `Traducción: "`+text2+`"`, total_translations, flipClasses);
	else
		text_to_repeat = createFlipHTML('Press the button to listen the answer', 'Pulsa el botón para escuchar la respuesta', total_translations, flipClasses);
	
	html_repeat_phrase = `
	<div class="row mt-3 fs-5" id="repeat_phrase_`+ repeat_phrase.id + `" >
	<!-- Controls -->
	<div class="row my-3 text-center">
		<!-- Sound -->
		<div class="col-12 col-sm-5" id="volume_container_` + repeat_phrase.id + `">
			<div class="row text-center">
				<div class="col-2 d-inline-block align-middle">
					<span class"" ><i class='fas fa-volume-up'></i></span>
				</div>
				<div class="col-10 d-inline-block align-middle">
				<span class="align-middle">
					<input type="range" min="0" max="1" step="0.01" value="0.5" class="form-range custom-range volume-input d-none"
					id="volume_range_` + repeat_phrase.id + `">
				</span>
				</div>
			</div>
		</div>
	</div>

		<div class="col-12 col-md-8">
			<div class="row">
				<div class="col-12">
					<div class="col-12 text-center">
						<span class="fs-5 text-muted" name="listen_and_repeat" title="Press the sound icon to play">`+ text_to_repeat + `</span>
					</div>
					<span class="fs-5 text-muted d-inline-block" name="user_answer" title="Press the sound icon to play"></span>
					<p class="fs-5 text-success" name="feedback"></p>
				</div>
			</div>
		</div>
		<div class="col-12 col-md-4 my-1">
		<div class="row">
				<div class="col-6 text-center">
				Listen
				<div class="row">
					<div class="col-12 text-center play-audio-container">
						<button type="button" id="play_rp_slow_${repeat_phrase.id}" 
						onclick="readText(${repeat_phrase.id}, 'slow', 0.7)" title="Listen audio">
							<i class="svgi-turtle"></i>
						</button>

						<button type="button" id="play_rp_fast_${repeat_phrase.id}" 
						onclick="readText(${repeat_phrase.id}, 'fast', 1)" title="Listen audio">
							<i class="svgi-rabbit"></i>
						</button>
					</div>
				</div>
				</div>
				<div class="col-6 text-center">
				Repeat
				<div class="row">
						<div class="col-12 text-center">
						<button class="btn shadow-none tool-icon mic-icon" 
						onclick="readVoice('repeat_phrase_`+ repeat_phrase.id + `')"
						name="mic_btn" title="Start to talk">
								<i class='fa-solid fa-microphone-slash'></i>
						</button>
						</div>
				</div>
				</div>
		</div>
		</div>
		<hr>
		<input name="database_id" value="`+repeat_phrase.id+`" hidden>
	</div><span id="exercises_area">`;

	document.getElementById("exercises_area").outerHTML = html_repeat_phrase;

	let btn_rp = document.getElementById("volume_container_"+repeat_phrase.id);
	btn_rp.addEventListener('mouseenter', (e) => {
		document.getElementById("volume_range_"+repeat_phrase.id).classList.add("d-block");
		document.getElementById("volume_range_"+repeat_phrase.id).classList.remove("d-none");
	});

	btn_rp.addEventListener('mouseleave', (e) => {
		document.getElementById("volume_range_"+repeat_phrase.id).classList.add("d-none");
		document.getElementById("volume_range_"+repeat_phrase.id).classList.remove("d-block");
	});

	
}
