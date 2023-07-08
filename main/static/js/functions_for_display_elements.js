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
// Image
function renderImage(image) {
	let src = image.image;
	document.querySelector(".new_element").outerHTML =
		`
		<div class="row exercise-sep">
			<div class="col-12">
				<div style="display:flex; justify-content:center; width:100%; margin:1rem 0;">
					<img class="box-shadow" src="${src}" alt="No se pudo cargar la imagen"
					style="max-height:450px; max-width:100%;">
				</div>
			</div>
		</div>
	`;
}
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

	document.querySelector(".new_element").outerHTML =
		`
		<div class="video-showed">
			<iframe src="${validated_url}" class="video-frame" title="YouTube video player" frameborder="0"
				allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
				allowfullscreen></iframe>
		</div>
		`;
}

function renderAudio(audio) {
	let desc = '';
	if (audio.show_description) {
		desc = `
		<div class="text-center" style="margin-top:1rem;" id="audio_flip_description_${audio.id}">
			<div class="front px-1 styles-front">${audio.description}</div>
			<div class="back px-1 styles-back">${audio.t_description}</div>
		</div>
		`;
	}

	document.querySelector(".new_element").outerHTML =
		`
		<div class="row exercise-sep">
			<div class="col-12">
				${desc}
				<div style="display:flex; justify-content:center; width:100%; margin:1rem 0;">
					<audio controls id="audio_player_${audio.id}" controlsList="nodownload">
						<source src="" type="audio/mpeg">
					</audio>
				</div>
			</div>
		</div>
	`;
	let audio_player = document.getElementById('audio_player_' + audio.id);

	if (desc != '')
		document.getElementById('audio_flip_description_' + audio.id).flipText();

	// get the audio as blob
	fetch(audio.audio_file)
		.then(response => response.blob())
		.then(blob => {
			audio_player.volume = 0.5;
			audio_player.src = URL.createObjectURL(blob);
		})
		.catch(error => {
			console.error('Error fetching the audio file:', error);
		});
}

// Text
function renderText(text) {
	let text1 = text.language1.replace(/\n/g, '<span></span>|');
	let text2 = text.language2.replace(/\n/g, '<span></span>|');

	document.querySelector(".new_element").outerHTML =
		`
		<div class="fs-5 mx-1" id="text_${text.id}">
			<div class="front px-1 styles-front">${text1}</div>
			<div class="back px-1 styles-back">${text2}</div>
		</div>
		`;
	document.getElementById('text_' + text.id).flipText();
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
	document.querySelector(".new_element").outerHTML =
		`
		<div class="row" style="color:rgba(0,0,0,0)"><br></div>
		<div class="fw-bold fs-5 dialogue-name" style="color:${dialogue.color};">
			<p>${dialogue.name}:</p>
		</div>
		`+ createFlipHTML(text1, text2, total_translations, flipClasses) + `
		`;
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

	document.querySelector(".new_element").outerHTML =
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
						onclick="readVoice('repeat_phrase_${repeat_phrase.id}')"
						name="mic_btn" title="Start to talk">
								<i class='fa-solid fa-microphone-slash'></i>
						</button>
						</div>
				</div>
				</div>
		</div>
		</div>
		
		<input name="database_id" value="${repeat_phrase.id}" hidden>
	</div>`;

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

	document.querySelector(".new_element").outerHTML =
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
		</div>
		`;
	let txta = document.querySelector('#spellcheck_' + spellcheck.id + ' textarea');
	makeAdjustable(txta);

	user_answers.push(new Exercise(spellcheck.type, spellcheck.id, ''));
	$('#spellcheck_' + spellcheck.id + ' textarea').on('input propertychange', (e) => {
		let search = user_answers.find(e => e.id === spellcheck.id);
		search.answer = e.target.value;
	});
}

function renderMCQuestion(question) {
	// Sort choices
	if (question.randomize_choices)
		question.choices.sort(() => Math.random() - 0.5);
	else
		question.choices.sort((a, b) => a.choice_number - b.choice_number);

	let choices_html = '';
	let choice_ids = [];
	let radios_ids = [];

	// Choices
	for (let c of question.choices) {
		choices_html += `
		<li class="choice_group_${question.id}">
			<div class="render-choice-container" name="correct" id="choice_${c.id}">
				<div class="radio-container">
					<div class="radio-btn" id="radio_${c.id}">
						<i class="fa-solid fa-check"></i>
					</div>
				</div>
				<div class="translation-container translate_mcq_${question.id}">
					<p class="front styles-front px-1">${c.text}</p>
					<p class="back styles-back px-1">${c.t_text}</p>
				</div>
			</div>
		</li>
		`;
		choice_ids.push('choice_' + c.id);
		radios_ids.push('radio_' + c.id);
	}

	// Question
	document.querySelector(".new_element").outerHTML =
		`
		<div class="row mt-3 fs-5 exercise-sep" id="mc_question_${question.id}">
			<div class="col-12">
				<h3 class="fs-4 text-center translate_mcq_${question.id}">
					<p class="front styles-front px-1 fw-bold">Answer</p>
					<p class="back styles-back px-1 fw-bold">Contesta</p>
				</h3>
			</div>
			<div class="col-12">
				<div class="row">
					<div class="fst-italic text-dark text-start my-3 title translate_mcq_${question.id}">
						<p class="front styles-front px-1 fw-bold">${question.text}</p>
						<p class="back styles-back px-1 fw-bold">${question.t_text}</p>
					</div>
				</div>
				<div class="row">
					<ul class="render-choice">
						${choices_html}
					</ul>
				</div>
				
				<div class="row">
					<span class="fs-5 text-muted mb-2 d-none"> <strong>Your answer:</strong> </span>
				</div>
			</div>
		</div>
		`;
	// Add exercise for answer
	user_answers.push(new Exercise(question.type, question.id, ''));

	let translate = document.getElementsByClassName('translate_mcq_' + question.id);
	for (let t of translate)
		t.flipText();

	// Set functionality when click empty inside container
	for (let id of choice_ids) {
		document.getElementById(id).addEventListener('click', (e) => {
			if (e.target === document.getElementById(e.target.id)) {
				let choices_group = document.getElementsByClassName('choice_group_' + question.id);
				for (let cg of choices_group) {
					cg.querySelector('[name = correct]').classList.remove('checked');
					cg.querySelector('.radio-btn').classList.remove('selected');
				}
				let choice = e.target;
				choice.classList.add('checked');
				choice.querySelector('.radio-btn').classList.add('selected');

				// Put value into the object
				let search = user_answers.find(e => e.id === question.id);
				search.answer = e.target.id.replace('choice_', '');
			}
		});
	}

	// Set functionality when click radio
	for (let id of radios_ids) {
		document.getElementById(id).addEventListener('click', (e) => {
			let choices_group = document.getElementsByClassName('choice_group_' + question.id);
			for (let cg of choices_group) {
				cg.querySelector('[name = correct]').classList.remove('checked');
				cg.querySelector('.radio-btn').classList.remove('selected');
			}
			let choice = e.target.parentElement.parentElement;
			choice.classList.add('checked');
			choice.querySelector('.radio-btn').classList.add('selected');

			// Put value into the object
			let search = user_answers.find(e => e.id === question.id);
			search.answer = e.target.parentElement.id.replace('radio_', '');
		});
	}

}
