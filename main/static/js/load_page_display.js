// Switch for load element
function loadElement(element, total_translations) {
  switch (element.type) {
    case "image":
      renderImage(element);
      break;
    case "video":
      renderVideo(element);
      break;
    case "audio":
      renderAudio(element);
      break;
    case "text":
      renderText(element);
      break;
    case "dialogue":
      renderDialogue(element, total_translations);
      break;
    case "repeat_phrase":
      renderRepeatPhrase(element, total_translations);
      break;
    case "spellcheck":
      renderSpellcheck(element, total_translations);
      break;
    case "mc_question":
      renderMCQuestion(element);
      break;
  }
}
// End of switch for load element

function loadTemplate1(total_translations) {
  if (page.images[0] != undefined) {
    default_cover = page.images[0].image;
  }
  let img_showed = document.getElementById('img_showed');
  if (img_showed != null) {
    img_showed.setAttribute('src', default_cover);
    img_showed.classList.remove('d-none');
  }

  document.getElementById("answer_questions_message").flipText();
  sortCollections();

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
    document.getElementById("content_area").outerHTML = `
        <div class="new_element"></div>
        <div id="content_area"></div>`;
    loadElement(c, total_translations);
  }

  for (let e of exercises) {
    document.getElementById("exercises_area").outerHTML = `
        <div class="new_element"></div>
        <div id="exercises_area"></div>`;
    loadElement(e, total_translations);
  }

  setFunctionality(total_translations);
}

function loadTemplate2(total_translations) {
  document.getElementById("answer_questions_message").flipText();
  sortCollections();

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
    document.getElementById("content_area").outerHTML = `
        <div class="new_element"></div>
        <div id="content_area"></div>`;
    loadElement(c, total_translations);
  }

  for (let e of exercises) {
    document.getElementById("exercises_area").outerHTML = `
        <div class="new_element"></div>
        <div id="exercises_area"></div>`;
    loadElement(e, total_translations);
  }

  setFunctionality(total_translations);
}

function loadTemplate3(total_translations) {
  sortCollections();
  for (let e of collections_sorted) {
    document.querySelector('.new_element').outerHTML = `
    <div class="new_element"></div>
    <div class="new_element"></div>`;
    loadElement(e, total_translations);
  }
  setFunctionality(total_translations);
}



/* Load page */

// Set subtitle
let page_subtitle = document.getElementById("subtitle");
if (page_subtitle != null)
  page_subtitle.flipText();

switch (parseInt(page_type)) {
  case 1:
    loadTemplate1(total_translations);
    break;
  case 2:
    loadTemplate2(total_translations);
    break;
  case 3:
    loadTemplate3(total_translations);
    break;
}