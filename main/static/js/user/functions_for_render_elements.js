// Contents
function renderDialogue(dialogue, total_translations) {
    let html_dialogue = ``;
    let text1 = dialogue.content1.replace(/\n/g, '<span></span>|');
    let text2 = dialogue.content2.replace(/\n/g, '<span></span>|');

    let flipClasses = {
        "paper": "fs-5 mx-1",
        "front": "px-1",
        "back": "px-1"
    };
    html_dialogue += `
    <div class="row" style="color:rgba(0,0,0,0)"><br></div>
    <div class="fw-bold fs-5 dialogue-name" style="color:`+ dialogue.color + `;">
        <p>`+ dialogue.name + `:</p>
    </div>
    `+ createFlipHTML(text1, text2, total_translations, flipClasses) + `
    <div id="content_area"></div>`;

    document.getElementById("content_area").outerHTML = html_dialogue;
}

// Exercises
function renderRepeatPhrase(repeat_phrase, total_translations) {
    let html_repeat_phrase = ``;
    let text_clean = repeat_phrase.content1.replace(/[|]/g, ' ');
    let text1 = repeat_phrase.content1.replace(/\n/g, '<span></span>|');
    let text2 = repeat_phrase.content2.replace(/\n/g, '<span></span>|');
    let flipClasses = {
        "paper": "mx-1",
        "front": "px-1",
        "back": "px-1"
    };
    html_repeat_phrase = `
    <div class="row mt-3 fs-5" id="repeat_phrase_`+ repeat_phrase.id + `" text_answer = "` + text_clean + `">
        <div class="col-12 col-md-8">
        `+ createFlipHTML(text1, text2, total_translations, flipClasses) + `
        <div class="row">
            <div class="col-12">
            <p class="fs-5 text-muted" name="user_answer"><strong>Listen and repeat:</strong> "`+ text_clean + `"</p>
            <p class="fs-5 text-success" name="feedback"></p>
            </div>
        </div>
        </div>
        <div class="col-12 col-md-4 my-1">
        <div class="row">
            <div class="col-6 text-center">
            Listen
            <div class="row">
                <div class="col-12 text-center">
                <button class="btn shadow-none tool-icon sound_icon" 
                onclick="readText('repeat_phrase_` + repeat_phrase.id + `')"
                name="sound_btn" title="Listen audio">
                    <i class='fas fa-volume-up'></i>
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
        <hr>
        <input name="database_id" value="`+repeat_phrase.id+`" hidden>
    </div><span id="exercises_area">`;

    document.getElementById("exercises_area").outerHTML = html_repeat_phrase;
}
