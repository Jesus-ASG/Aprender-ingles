// Functions for load elements
function loadImage(image) {
  addImage();
  let html_image = document.getElementById('element_' + (max_elem - 1));
  let preview = html_image.querySelector('[name = preview]');

  html_image.querySelector('[name = id]').value = image.id;
  html_image.querySelector('[name = default_image]').value = media_url + image.image;

  preview.setAttribute('src', media_url + image.image);
  preview.classList.remove('d-none');
}

function loadVideo(video) {
  if (page_type == 2)
    addVideo(false);
  else
    addVideo();
  let html_video = document.getElementById("element_" + (max_elem - 1));
  html_video.querySelector('[name = id]').value = video.id;
  html_video.querySelector('[name = url]').value = video.url;
  verifyVideo(max_elem - 1);
}

function loadAudio(audio) {
  addAudio();
  let html_audio = document.getElementById('element_' + (max_elem - 1));
  let audio_player = html_audio.querySelector('[name = audio_player]');

  html_audio.querySelector('[name = id]').value = audio.id;
  html_audio.querySelector('[name = default_audio]').value = media_url + audio.audio_file;
  html_audio.querySelector('[name = label_name]').value = audio.label_name;
  html_audio.querySelector('[name = show_description]').checked = audio.show_description;
  html_audio.querySelector('[name = description]').value = audio.description;
  html_audio.querySelector('[name = t_description]').value = audio.t_description;

  if (audio.show_description)
    html_audio.querySelector('[name = description_container]').classList.remove('d-none')

  // get the audio as blob
  fetch(media_url + audio.audio_file)
    .then(response => response.blob())
    .then(blob => {
      audio_player.volume = 0.5;
      audio_player.src = URL.createObjectURL(blob);
    })
    .catch(error => {
      console.error('Error fetching the audio file:', error);
    });

}

function loadText(text) {
  addText();
  let html_text = document.getElementById("element_" + (max_elem - 1));

  html_text.querySelector('[name = id]').value = text.id;
  html_text.querySelector('[name = language1]').value = text.language1;
  html_text.querySelector('[name = language2]').value = text.language2;
}

function loadDialogue(dialogue) {
  // add dialogue increases in 1 the id
  addDialogue();
  let html_dialogue = document.getElementById("element_" + (max_elem - 1));

  html_dialogue.querySelector('[name = id]').value = dialogue.id;
  html_dialogue.querySelector('[name = name]').value = dialogue.name;
  html_dialogue.querySelector('[name = color]').value = dialogue.color;
  html_dialogue.querySelector('[name = language1]').value = dialogue.content1;
  html_dialogue.querySelector('[name = language2]').value = dialogue.content2;

  $(".ch-color_" + (max_elem - 1)).css({ 'color': dialogue.color });
}

function loadRepeatPhrase(repeat_phrase) {
  repeatPhrase();
  let html_repeat_phrase = document.getElementById("element_" + (max_elem - 1));

  html_repeat_phrase.querySelector('[name = id]').value = repeat_phrase.id;
  html_repeat_phrase.querySelector('[name = language1]').value = repeat_phrase.content1;
  html_repeat_phrase.querySelector('[name = language2]').value = repeat_phrase.content2;
  html_repeat_phrase.querySelector('[name = show_text]').checked = repeat_phrase.show_text;
}

function loadSpellcheck(spellcheck) {
  addSpellcheck();
  let html_spellcheck = document.getElementById("element_" + (max_elem - 1));

  html_spellcheck.querySelector('[name = id]').value = spellcheck.id;
  html_spellcheck.querySelector('[name = wrong_text]').value = spellcheck.wrong_text;
  html_spellcheck.querySelector('[name = right_text]').value = spellcheck.right_text;
  html_spellcheck.querySelector('[name = translated_right_text]').value = spellcheck.translated_right_text;
}

function loadMCQuestion(question) {
  let util = addMultipleChoiceQuestion();
  let html_question = document.getElementById("element_" + (max_elem - 1));

  html_question.querySelector('[name = id]').value = question.id;
  html_question.querySelector('[name = text]').value = question.text;
  html_question.querySelector('[name = t_text]').value = question.t_text;
  html_question.querySelector('[name = randomize_choices]').checked = question.randomize_choices;

  // For load choices
  for (let c of question.choices) {
    document.getElementById(util.add_choice_id).click();
  }

  // Sort choices by choice_number
  question.choices.sort((a, b) => a.choice_number - b.choice_number);
  // Choices dom object
  let cd = document.querySelectorAll("#element_" + (max_elem - 1) + " .choice");

  for (let i = 0; i < question.choices.length; i++) {
    cd[i].querySelector('[name = id]').value = question.choices[i].id;
    cd[i].querySelector('[name = text]').value = question.choices[i].text;
    cd[i].querySelector('[name = t_text]').value = question.choices[i].t_text;

    if (question.choices[i].correct) {
      cd[i].querySelector('[name = correct]').classList.add('checked');
      cd[i].querySelector('.radio-btn').classList.add('selected');
    }
  }
}
// End of functions for load elements

// Switch for load element
function loadElement(element) {
  switch (element.type) {
    case "image":
      loadImage(element);
      break;
    case "video":
      loadVideo(element);
      break;
    case "audio":
      loadAudio(element);
      break;
    case "text":
      loadText(element);
      break;
    case "dialogue":
      loadDialogue(element);
      break;
    case "repeat_phrase":
      loadRepeatPhrase(element);
      break;
    case "spellcheck":
      loadSpellcheck(element);
      break;
    case "mc_question":
      loadMCQuestion(element);
      break;
  }
}
// End of switch for load element

function loadNewTemplate1() {
  if (db_images[0] != undefined)
    default_cover = media_url + db_images[0].image;
  document.getElementById('img_showed').setAttribute('src', default_cover);
}

function loadTemplate1() {
  if (db_images[0] != undefined) {
    default_cover = media_url + db_images[0].image;
    document.querySelector('[name = images]').querySelector('[name = id]').value = db_images[0].id;
  }
  document.getElementById('img_showed').setAttribute('src', default_cover);

  let contents = [];
  let exercises = [];
  for (let element of collections_sorted) {
    if (element.is_exercise)
      exercises.push(element);
    else
      contents.push(element);
  }

  for (let c of contents) {
    if (c.type == "image")
      continue;
    c.element_number = max_elem;
    document.getElementById("content_area").outerHTML = `
      <div class="new_element"></div>
      <div id="content_area"></div>`;
    loadElement(c);
  }

  for (let e of exercises) {
    e.element_number = max_elem;
    document.getElementById("exercises_area").outerHTML = `
      <div class="new_element"></div>
      <div id="exercises_area"></div>`;
    loadElement(e);
  }
}

function loadNewTemplate2() {
  document.getElementById("content_area").outerHTML = `
    <div class="new_element"></div>
    <div id="content_area"></div>`;
  addVideo(false);
}

function loadTemplate2() {
  let contents = [];
  let exercises = [];
  for (let element of collections_sorted) {
    if (element.is_exercise)
      exercises.push(element);
    else
      contents.push(element);
  }

  for (let c of contents) {
    c.element_number = max_elem;
    document.getElementById("content_area").outerHTML = `
      <div class="new_element"></div>
      <div id="content_area"></div>`;
    loadElement(c);
  }

  for (let e of exercises) {
    e.element_number = max_elem;
    document.getElementById("exercises_area").outerHTML = `
      <div class="new_element"></div>
      <div id="exercises_area"></div>`;
    loadElement(e);
  }
}

function loadTemplate3() {
  for (let e of collections_sorted) {
    e.element_number = max_elem;
    document.querySelector('.new_element').outerHTML = `
      <div class="new_element"></div>
      <div class="new_element"></div>`;
    loadElement(e);
  }
}

function loadPage() {
  switch (parseInt(page_type)) {
    case 1:
      loadTemplate1();
      break;
    case 2:
      loadTemplate2();
      break;
    case 3:
      loadTemplate3();
      break;
  }
}


/* Load page */
if (page_id !== "") { // page id is provided
  sortCollections();
  loadPage();
}
else { // is a new page
  switch (parseInt(page_type)) {
    case 1:
      loadNewTemplate1();
      break;
    case 2:
      loadNewTemplate2();
      break;
  }
}
