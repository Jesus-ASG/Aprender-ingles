// if there are answers in the page
if (db_answers.length > 0) {
	// Check if is sumbited
	let submited = db_answers[0].submited;
	if (submited) {
		showUserAnswers(db_answers, true);
		showStatistics(db_score);
	}
	else
		showUserAnswers(db_answers, false);
}

let speaking_currently = false;
let waiting_for_voice = false;
let listening_currently = false;

let highlighted_sound_btn = null;
let highlighted_mic_btn = null;
let answer_paragraph = null;

let db_exercise_id = 0;

const speech = new SpeechSynthesisUtterance();
window.speechSynthesis.cancel();

const SpeechRecognition = window.SpeechRecognition || webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.continuous = true;
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

// Voice input 
recognition.onstart = (e) => {
	listening_currently = true;
}
recognition.onend = (e) => {
	listening_currently = false;
	highlighted_mic_btn.classList.remove("highlighted-icon");
}
recognition.onresult = (e) => {
	let transcript = "";
	for (var i = e.resultIndex; i < e.results.length; ++i)
		if (e.results[i].isFinal)
			transcript += e.results[i][0].transcript;

	let search = user_answers.find(e => e.id === parseInt(db_exercise_id));
	transcript = capitalizeFirstLetter(transcript);
	search.answer = transcript;
	answer_paragraph.innerHTML = `<strong>Your answer:</strong> "${transcript}"`;
}
recognition.error = (e) => { }

function readVoice(element_id) {
	if (!listening_currently) {
		listening_currently = true;
		let elem = document.getElementById(element_id);
		answer_paragraph = elem.querySelector("[name = user_answer]");
		highlighted_mic_btn = elem.querySelector("[name = mic_btn]");
		db_exercise_id = elem.querySelector("[name = database_id]").value;

		highlighted_mic_btn.classList.add("highlighted-icon");

		icon = highlighted_mic_btn.querySelector("i");
		icon.classList.remove("fa-solid", "fa-microphone-slash");
		icon.classList.add("fas", "fa-microphone");

		recognition.start();
	} else {
		highlighted_mic_btn.classList.remove("highlighted-icon");

		icon = highlighted_mic_btn.querySelector("i");
		icon.classList.remove("fas", "fa-microphone");
		icon.classList.add("fa-solid", "fa-microphone-slash");

		recognition.stop();
	}
}

// Voice output
speech.onstart = (e) => {
	speaking_currently = true;
}
speech.onend = (e) => {
	speaking_currently = false;
	highlighted_sound_btn.classList.remove("icon-active");
}

function readText(id, speed, rate) {
	if (!speaking_currently) {
		speaking_currently = true;

		const csrftoken = getCookie('csrftoken');
		$.ajax({
			type: "POST",
			url: URL_REQUEST_EXERCISE_ANSWER,
			data: {
				'exercise_type': 'repeat_phrase',
				'exercise_id': id
			},
			headers: { "X-CSRFToken": csrftoken },
			success: function (response) {
				if (response.success) {
					text_clean = response.response.replace(/[|]/g, ' ');
					speech.text = text_clean;
					speech.volume = document.querySelector('.volume-input').value;
					speech.lang = 'en-US';
					speech.rate = rate;
					speech.pitch = 1;
					window.speechSynthesis.speak(speech);

					highlighted_sound_btn = document.getElementById(`play_rp_${speed}_${id}`);
					highlighted_sound_btn.classList.add("icon-active");
				}
			},
			error: function (response) { }
		});
	}
}


function setVolumeFunctionality() {
	$(".volume-input").on('input', (e) => {
		$(".volume-input").val(e.target.value);
		speech.volume = e.target.value;
	});
}


function capitalizeFirstLetter(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}


function saveAnswers(submit, show_feedback) {
	// Read all repeat phrases exersices
	let formData = new FormData();

	let evaluate = false;
	if (LAST_PAGE && submit)
		evaluate = true;

	formData.append("evaluate", evaluate.toString());
	formData.append("submit", submit.toString());
	formData.append("answers", JSON.stringify(user_answers));

	const csrftoken = getCookie('csrftoken');
	$.ajax({
		type: "POST",
		url: URL_ANSWER_PAGE,
		data: formData,
		processData: false,
		contentType: false,
		headers: { "X-CSRFToken": csrftoken },
		success: function (response) {
			//console.log(response);
			showUserAnswers(response.answers, show_feedback);
			showStatistics(response.results);
		},
		error: function (response) { }
	});
}

function showUserAnswers(answers, show_feedback) {
	if (!answers)
		return;

	if (show_feedback) {
		document.getElementById("btn_send_answers").outerHTML = `
		<a href="` + URL_NEXT_PAGE + `" type="button" class="btn btnr-f-orange fs-5">
		Continue / Continuar
		</a>
		`;
		$('button[name="mic_btn"]').attr("disabled", true);
	}

	for (let answer of answers) {
		switch (answer.type) {
			case "repeat_phrase":
				let rp = document.getElementById("repeat_phrase_" + answer.exercise_id);
				let rp_ans = rp.querySelector("[name = user_answer]");
				let feedback = rp.querySelector("[name = feedback]");

				rp_ans.innerHTML = `<strong>Your answer:</strong> "${answer.answer}"`;
				if (show_feedback) {
					feedback.innerHTML = `<strong>Right answer:</strong> "${answer.feedback}"`;
				}
				break;
			case "spellcheck":
				let spc = document.getElementById("spellcheck_" + answer.exercise_id);
				if (show_feedback) {
					spc.querySelector('span').innerText = `Your answer: "${answer.answer}"`;
					spc.querySelector('textarea').outerHTML =
						` <br>
					<span class="fs-5 text-success mb-2"> <strong>Right answer: "${answer.feedback}"</strong> </span>
					`;
				} else {
					spc.querySelector('textarea').value = answer.answer;
				}
				break;
		}
	}
}

function showStatistics(results) {
	if (!hasContent(results))
		return;
	let results_dom = document.getElementById("results");
	results_dom.classList.remove("d-none");
	let score_lbl1 = `Score`;
	let score_lbl2 = `Puntaje`;

	let writing = results_dom.querySelector("[name = writing]");
	let comprehension = results_dom.querySelector("[name = comprehension]");
	let speaking = results_dom.querySelector("[name = speaking]");

	let writing_progress = writing.querySelector(".linear-progress-value");
	let comprehension_progress = comprehension.querySelector(".linear-progress-value");
	let speaking_progress = speaking.querySelector(".linear-progress-value");

	// Titles
	results_dom.querySelector(".statistics-container .label h3").innerText = results.letter_grade;

	results_dom.querySelector("[name = title_score]").innerHTML = createFlipHTML(score_lbl1, score_lbl2, total_translations);
	writing.querySelector("[name = title]").innerHTML = createFlipHTML("Writing", "Escritura", total_translations);
	comprehension.querySelector("[name = title]").innerHTML = createFlipHTML("Comprehension", "Comprensión", total_translations);
	speaking.querySelector("[name = title]").innerHTML = createFlipHTML("Speaking", "Pronunciación", total_translations);

	// Values
	writing_progress.style.width = `${results.writing_percentage}%`;
	comprehension_progress.style.width = `${results.comprehension_percentage}%`;
	speaking_progress.style.width = `${results.speaking_percentage}%`;

	// Info about percentage
	writing_progress.parentElement.title = `${results.writing_percentage}%`;
	comprehension_progress.parentElement.title = `${results.comprehension_percentage}%`;
	speaking_progress.parentElement.title = `${results.speaking_percentage}%`;

	results_dom.querySelector('.statistic-title').innerText = `${results.score_percentage} / 100`;

	let score_bar_dom = document.querySelector('#score_circle_progress .basic-progress-level');
	let end_value = parseInt(results.score_percentage) || 0;
	progressAnimation(score_bar_dom, end_value);
	setFunctionality(total_translations);
}