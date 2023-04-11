/* Sort collections from database */
let collections_sorted = [];
/* Contents */
// Images
if (db_images.length > 0)
	for (let image of db_images) {
		image.type = "image";
		image.is_exercise = false;
		collections_sorted.push(image);
	}

// Texts
if (db_texts.length > 0) {
	for (let text of db_texts) {
		text.type = "text";
		text.is_exercise = false;
		collections_sorted.push(text);
	}
}

// Dialogues
if (db_dialogues.length > 0)
	for (let dialogue of db_dialogues) {
		dialogue.type = "dialogue";
		dialogue.is_exercise = false;
		collections_sorted.push(dialogue);
	}

/* Exercises */
// Repeat phrases
if (db_repeat_phrases.length > 0)
	for (let repeat_phrase of db_repeat_phrases) {
		repeat_phrase.type = "repeat_phrase";
		repeat_phrase.is_exercise = true;
		collections_sorted.push(repeat_phrase);
	}

if (db_spellchecks.length > 0)
	for (let spellcheck of db_spellchecks) {
		spellcheck.type = "spellcheck";
		spellcheck.is_exercise = true;
		collections_sorted.push(spellcheck);
	}

// Sort
collections_sorted.sort((a, b) => a.element_number - b.element_number);