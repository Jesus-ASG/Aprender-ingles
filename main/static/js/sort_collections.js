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
// Sort
collections_sorted.sort((a, b) => a.element_number - b.element_number);