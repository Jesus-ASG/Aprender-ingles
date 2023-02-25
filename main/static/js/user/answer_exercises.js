class StoryAnswers{
	constructor(id, pages){
		this.id = parseInt(id);
		this.pages = pages;
	}
}

class PageAnswers{
	constructor(id, exercises){
		this.id = parseInt(id);
		this.exercises = exercises;
	}
	toString(){
		return `Id-> ${this.id}, Exercises-> ${this.exercises}`;
	}
}

class Exercise{
	constructor(type, id, answer){
		this.type = type;
		this.id = parseInt(id);
		this.answer = answer;
	}
	toString(){
		return `Type-> ${this.type} Id-> ${this.id}, Answer-> ${this.answer}`;
	}
}

// creates object story
let story_answers = new StoryAnswers(db_story_id, []);
// Creates object for current page answers
let page_answers = new PageAnswers(db_page_id, []);
// Fill current page answers with exercises from database
for (let element of collections_sorted)
	if (element.is_exercise)
		page_answers.exercises.push(new Exercise(element.type, element.id, ''));

let ls_story_answers = JSON.parse(localStorage.getItem('story_answers_'+ db_story_id));
if (ls_story_answers){
	let current_page = ls_story_answers.pages.find(e => e.id === parseInt(db_page_id));
	if (current_page)
		sendAnswers();
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
	
	let search = page_answers.exercises.find(e => e.id === parseInt(db_exercise_id));
	
	transcript = capitalizeFirstLetter(transcript)
	search.answer = transcript + ".";
	answer_paragraph.innerHTML = `<strong>Your answer:</strong> "${transcript}."`;
}
recognition.error = (e) => {}

function readVoice(element_id){
	if (!listening_currently){
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
	}else{
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

function readText(id, speed, rate){
	if (!speaking_currently){
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
						if (response.success){
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
				error: function (response) {}
		});
	}
}


function setVolumeFunctionality(){
	$(".volume-input").on('input', (e)=>{
		$(".volume-input").val(e.target.value);
		speech.volume = e.target.value;
	});
}


function capitalizeFirstLetter(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}

function sendAnswers(){
	let ls_story_answers = JSON.parse(localStorage.getItem('story_answers_'+ db_story_id));
	if (ls_story_answers){
		let search = ls_story_answers.pages.find(e => e.id === parseInt(db_page_id));
		if(search){
			//console.log("answers from this page have already been sent");
			// just ask for feedback
		}
		else{
			ls_story_answers.pages.push(page_answers);
			//localStorage.removeItem('story_answers');
			localStorage.setItem('story_answers_'+ db_story_id, JSON.stringify(ls_story_answers));
		}
	}
	else{
		// this is the first page, so it is pushed
		story_answers.pages.push(page_answers);
		localStorage.setItem('story_answers_'+ db_story_id, JSON.stringify(story_answers));
	}

	let clear_storage_on_click = (LAST_PAGE) ? 'onclick="clearStoryAnswersLocalStorage()"' : '';

	let html_button = `
	<a `+ clear_storage_on_click +` href="`+URL_NEXT_PAGE+`" type="button" class="btn btnr-f-orange fw-bold fs-5">
        Continue / Continuar
    </a>
	`;
	document.getElementById("btn_send_answers").outerHTML = html_button;
	
	let formData = new FormData();
	// Tell if request will going to evaluate
	let to_evaluate = false;
	if (LAST_PAGE)
		to_evaluate = true;
	formData.append("evaluate", to_evaluate.toString());

	// Tell what is the current page
	formData.append("feedback_page_id", db_page_id);
	
	// update ls_story answers
	ls_story_answers = JSON.parse(localStorage.getItem('story_answers_'+ db_story_id));
	formData.append("story_answers", JSON.stringify(ls_story_answers))
	
	
	const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: URL_ANSWER_PAGE,
        data: formData,
        processData: false,
        contentType: false,
        headers: { "X-CSRFToken": csrftoken },
        success: function (response) {
            showFeedback(response);
        },
        error: function (response) {}
    });
}

function showFeedback(response){
	let current_page = response.pages.find(e => e.id === parseInt(db_page_id));
	if (current_page){
		$('button[name="mic_btn"]').attr("disabled", true);
		for(let exercise of current_page.exercises){
			switch (exercise.type){
				case "repeat_phrase":
					let rp = document.getElementById("repeat_phrase_"+exercise.id);
					let rp_ans = rp.querySelector("[name = user_answer]");
					let feedback = rp.querySelector("[name = feedback]");

					rp_ans.innerHTML = `<strong>Your answer:</strong> "${exercise.answer}"`;
					feedback.innerHTML = `<strong>Right answer:</strong> "${exercise.feedback}"`;
					break;
			}
		}
	}

	let results = response.score;
	if(results){
		let flipClasses = {
			"paper": "mx-1",
			"front": "px-1",
			"back": "px-1"
		};
		let results_dom = document.getElementById("results");
		results_dom.classList.remove("d-none");
		let score_lbl1 = `Results: ${results.score}pts`;
		let score_lbl2 = `Resultados: ${results.score}pts`;

		let comprehension = results_dom.querySelector("[name = comprehension]");
		let writing = results_dom.querySelector("[name = writing]");
		let speaking = results_dom.querySelector("[name = speaking]");

		let comprehension_progress =  comprehension.querySelector("[name = progress]");
		let writing_progress = writing.querySelector("[name = progress]");
		let speaking_progress = speaking.querySelector("[name = progress]");

		// Titles
		results_dom.querySelector("[name = letter_grade]").innerText = results.letter_grade;
		results_dom.querySelector("[name = title_score]").innerHTML = createFlipHTML(score_lbl1, score_lbl2, total_translations, flipClasses);
		comprehension.querySelector("[name = title]").innerHTML = createFlipHTML("Comprehension", "Comprensión", total_translations, flipClasses);
		writing.querySelector("[name = title]").innerHTML = createFlipHTML("Writing", "Escritura", total_translations, flipClasses);
		speaking.querySelector("[name = title]").innerHTML = createFlipHTML("Speaking", "Pronunciación", total_translations, flipClasses);
		
		// Values
		comprehension_progress.style.width = `${results.comprehension_percentage}%`;
		comprehension_progress["aria-valuenow"] = `${results.comprehension_percentage}%`;

		writing_progress.style.width = `${results.writing_percentage}%`;
		writing_progress["aria-valuenow"] = `${results.writing_percentage}%`;

		speaking_progress.style.width = `${results.speaking_percentage}%`;
		speaking_progress["aria-valuenow"] = `${results.speaking_percentage}%`;

		setFunctionality(total_translations);
	}
}

function clearStoryAnswersLocalStorage(){
	localStorage.removeItem('story_answers_'+ db_story_id)
}