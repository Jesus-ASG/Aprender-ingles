let speaking_currently = false;
let waiting_for_voice = false;
let listening_currently = false;

let highlighted_sound_btn = null;
let highlighted_mic_btn = null;
let answer_paragraph = null;

const speech = new SpeechSynthesisUtterance();

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
	
	answer_paragraph.innerText = capitalizeFirstLetter(transcript);
}
recognition.error = (e) => {
	//console.log(e.error);
}

function readVoice(element_id){
	if (!listening_currently){
		listening_currently = true;
		let elem = document.getElementById(element_id);
		answer_paragraph = elem.querySelector("[name = answer]");
		highlighted_mic_btn = elem.querySelector("[name = mic_btn]");
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
	highlighted_sound_btn.classList.remove("highlighted-icon");
}

function readText(element_id){
	if (!speaking_currently){
		speaking_currently = true;
		let elem = document.getElementById(element_id);
		let text = elem.getAttribute("text_answer");
		highlighted_sound_btn = elem.querySelector("[name = sound_btn]");
		highlighted_sound_btn.classList.add("highlighted-icon");

		speech.lang = 'en-US';
		speech.text = text;
		speech.volume = 1;
		speech.rate = 1;
		speech.pitch = 1;
		window.speechSynthesis.speak(speech);
	}
}

document.addEventListener("DOMContentLoaded", function() {
	
});

/* Exersices */
/* Repeat phrases */

class Exersice{
	constructor(exersice_id, answer){
		this.exersice_id = exersice_id;
		this.answer = answer;
	}
	toString(){
		return `Id: ${this.exersice_id}, Answer: ${this.answer}`;
	}
}

class PageAnswers{
	constructor(page_id, exersices){}
}

function capitalizeFirstLetter(string) {
	return string.charAt(0).toUpperCase() + string.slice(1);
}