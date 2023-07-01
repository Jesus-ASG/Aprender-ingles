/* Sort collections from database */
let collections_sorted = [];
function sortCollections() {
	/* Contents */
	// Audios
	for (let audio of db_audios) {
		audio.type = "audio";
		audio.is_exercise = false;
		collections_sorted.push(audio);
	}

	// Videos
	for (let video of db_videos) {
		video.type = "video";
		video.is_exercise = false;
		collections_sorted.push(video);
	}

	// Images
	for (let image of db_images) {
		image.type = "image";
		image.is_exercise = false;
		collections_sorted.push(image);
	}

	// Texts
	for (let text of db_texts) {
		text.type = "text";
		text.is_exercise = false;
		collections_sorted.push(text);
	}

	// Dialogues
	for (let dialogue of db_dialogues) {
		dialogue.type = "dialogue";
		dialogue.is_exercise = false;
		collections_sorted.push(dialogue);
	}

	/* Exercises */
	// Repeat phrases
	for (let repeat_phrase of db_repeat_phrases) {
		repeat_phrase.type = "repeat_phrase";
		repeat_phrase.is_exercise = true;
		collections_sorted.push(repeat_phrase);
	}
	// Spellchecks
	for (let spellcheck of db_spellchecks) {
		spellcheck.type = "spellcheck";
		spellcheck.is_exercise = true;
		collections_sorted.push(spellcheck);
	}
	// Multiple Choice Questions
	for (let question of db_mc_questions) {
		question.type = "mc_question";
		question.is_exercise = true;
		collections_sorted.push(question);
	}

	// Sort
	collections_sorted.sort((a, b) => a.element_number - b.element_number);
}