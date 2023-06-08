class Exercise {
	constructor(type, id, answer) {
		this.type = type;
		this.id = parseInt(id);
		this.answer = answer;
	}
	toString() {
		return `Type-> ${this.type} Id-> ${this.id}, Answer-> ${this.answer}`;
	}
}

// General
let titleClasses = {
	"paper": "",
	"front": "px-1 fw-bold",
	"back": "px-1 fw-bold"
}

// Contents
// Video
function renderVideo(video) {

	validated_url = "";
	if (video.url.startsWith("https://www.youtube.com/embed/"))
		validated_url = video.url;
	else if (video.url.startsWith("https://www.youtube.com/watch?v=")) {
		code = video.url.split("https://www.youtube.com/watch?v=")[1];
		validated_url = "https://www.youtube.com/embed/" + code;
	}
	else if (video.url.startsWith("https://youtu.be/")) {
		code = video.url.split("https://youtu.be/")[1];
		validated_url = "https://www.youtube.com/embed/" + code;
	}

	document.getElementById("content_area").outerHTML =
		`
		<div class="video-showed">
			<iframe src="${validated_url}" class="video-frame" title="YouTube video player" frameborder="0"
				allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
				allowfullscreen></iframe>
		</div>
		<div id="content_area"></div>
	`;
}

// Text
function renderText(text, total_translations) {
	let text1 = text.language1.replace(/\n/g, '<span></span>|');
	let text2 = text.language2.replace(/\n/g, '<span></span>|');
	let flipClasses = {
		"paper": "fs-5 mx-1",
		"front": "px-1",
		"back": "px-1"
	};

	document.getElementById("content_area").outerHTML =
		createFlipHTML(text1, text2, total_translations, flipClasses) +
		`
	<div id="content_area"></div>
	`;
}

// Dialogue
function renderDialogue(dialogue, total_translations) {
	let text1 = dialogue.content1.replace(/\n/g, '<span></span>|');
	let text2 = dialogue.content2.replace(/\n/g, '<span></span>|');

	let flipClasses = {
		"paper": "fs-5",
		"front": "px-1",
		"back": "px-1"
	};
	document.getElementById("content_area").outerHTML =
		`
	<div class="row" style="color:rgba(0,0,0,0)"><br></div>
	<div class="fw-bold fs-5 dialogue-name" style="color:${dialogue.color};">
		<p>${dialogue.name}:</p>
	</div>
	`+ createFlipHTML(text1, text2, total_translations, flipClasses) + `
	<div id="content_area"></div>`;
}

// Exercises
function renderRepeatPhrase(repeat_phrase, total_translations) {
	let text1 = repeat_phrase.content1.replace(/\n/g, '<span></span>|').trim();
	let text2 = repeat_phrase.content2.replace(/\n/g, '<span></span>|').trim();
	let flipClasses = {
		"paper": "fst-italic text-dark",
		"front": "px-1",
		"back": "px-1"
	};
	let text_to_repeat = '';
	if (repeat_phrase.show_text)
		text_to_repeat = createFlipHTML(`Repeat: "` + text1 + `"`, `Traducción: "` + text2 + `"`, total_translations, flipClasses);
	else
		text_to_repeat = createFlipHTML('Press the button to listen the answer', 'Pulsa el botón para escuchar la respuesta', total_translations, flipClasses);

	document.getElementById("exercises_area").outerHTML =
		`
	<div class="row mt-3 fs-5 exercise-sep" id="repeat_phrase_${repeat_phrase.id}" >
	<div class="col-12">
			<h3 class="fs-4 text-center">${createFlipHTML('Listen and repeat', 'Escucha y repite', total_translations, titleClasses)}</h3>
		</div>
	<!-- Controls -->
	<div class="row my-3 text-center">
		<!-- Sound -->
		<div class="col-12 col-sm-5" id="volume_container_${repeat_phrase.id}">
			<div class="row text-center">
				<div class="col-2 d-inline-block align-middle icon-volume-range">
					<span><i class='fas fa-volume-up'></i></span>
				</div>
				<div class="col-10 d-inline-block align-middle">
				<span class="align-middle">
					<input type="range" min="0" max="1" step="0.01" value="0.5" class="form-range custom-range volume-input"
					id="volume_range_${repeat_phrase.id}">
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
		
		<input name="database_id" value="`+ repeat_phrase.id + `" hidden>
	</div><span id="exercises_area">`;

	let btn_rp = document.getElementById("volume_container_" + repeat_phrase.id);
	btn_rp.addEventListener('mouseenter', (e) => {
		document.getElementById("volume_range_" + repeat_phrase.id).style.opacity = 1;
	});

	btn_rp.addEventListener('mouseleave', (e) => {
		document.getElementById("volume_range_" + repeat_phrase.id).style.opacity = 0;
	});

	user_answers.push(new Exercise(repeat_phrase.type, repeat_phrase.id, ''));
}


function renderSpellcheck(spellcheck, total_translations) {
	let scriptClasses = {
		"paper": "fst-italic text-dark",
		"front": "px-1",
		"back": "px-1"
	};

	document.getElementById("exercises_area").outerHTML =

		`
	<div class="row mt-3 fs-5 exercise-sep" id="spellcheck_${spellcheck.id}">
		<div class="col-12">
			<h3 class="fs-4 text-center">`+ createFlipHTML('Spellcheck', 'Revisar ortografía', total_translations, titleClasses) + `</h3>
		</div>
		<div class="col-12">
			
			<p> ${createFlipHTML('Write and fix: "' + spellcheck.wrong_text + '"', 'Traducción: "' + spellcheck.translated_right_text + '"', total_translations, scriptClasses)} </p>
			
			<span class="fs-5 text-muted mb-2"> <strong>Your answer:</strong> </span>
			<textarea class="form-control mb-2 txta fs-5" type="text" placeholder="Write the fixed text"></textarea>
			
		</div>
	</div><span id="exercises_area">
	`;
	let txta = document.querySelector('#spellcheck_' + spellcheck.id + ' textarea');
	makeAdjustable(txta);

	user_answers.push(new Exercise(spellcheck.type, spellcheck.id, ''));
	$('#spellcheck_' + spellcheck.id + ' textarea').on('input propertychange', (e) => {
		let search = user_answers.find(e => e.id === spellcheck.id);
		search.answer = e.target.value;
	});
}

