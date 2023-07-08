let objects_deleted = {
    "images": [],
    "videos": [],
    "audios": [],
    "texts": [],
    "dialogues": [],
    "repeatPhrases": [],
    "spellchecks": [],
    "mc_questions": [],
    "question_choices": []
};

function deleteElement(id) {
    let element_to_delete = document.getElementById("element_" + id);
    let id_database = element_to_delete.querySelector('[name = id]').value;
    if (id_database) {
        let name = element_to_delete.getAttribute("name"); // IMPORTANT: NAME MUST BE EQUAL TO INSIDE OF objects_deleted
        objects_deleted[name].push(id_database);
    }
    element_to_delete.remove();

    let html = `
    <div class="alert alert-success alert-dismissible fade show mb-2 mt-2" role="alert">
        <div style="text-align: center;">
            <strong>Elemento eliminado correctamente</strong>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>`;
    document.getElementById("alert_removed_success").innerHTML = html;
}


function savePage() {
    let formData = new FormData();
    // Contents
    // Images
    let images = document.getElementsByName("images");
    let jsonImages = [];
    let image_counter = 0;
    for (let i of images) {
        let jsonI = {
            "id": i.querySelector('[name = id]').value,
            "element_number": i.querySelector('[name = element_number]').value,
            "file_key": ''
        }

        let image_file = i.querySelector('[name = image_file]').files[0];
        if (image_file != undefined) {
            let file_key = 'image_file_' + image_counter.toString();

            jsonI.file_key = file_key;
            formData.append(file_key, image_file);
            image_counter++;
        }

        jsonImages.push(jsonI);
    }

    // Videos
    let videos = document.getElementsByName('videos');
    let jsonVideos = [];
    for (let video of videos) {
        let jsonVideo = {
            "id": video.querySelector('[name = id]').value,
            "element_number": video.querySelector('[name = element_number]').value,
            "url": video.querySelector('[name = url]').value
        }
        jsonVideos.push(jsonVideo);
    }

    // Audios 
    let audios = document.getElementsByName("audios");
    let jsonAudios = [];
    let audios_counter = 0;
    for (let a of audios) {
        let jsonA = {
            "id": a.querySelector('[name = id]').value,
            "element_number": a.querySelector('[name = element_number]').value,

            "label_name": a.querySelector('[name = label_name]').value,
            "show_description": a.querySelector('[name = show_description]').checked,
            "description": a.querySelector('[name = description]').value,
            "t_description": a.querySelector('[name = t_description]').value,
            "file_key": ''
        }

        let audio_file = a.querySelector('[name = audio_file]').files[0];
        if (audio_file != undefined) {
            let file_key = 'audio_file_' + image_counter.toString();

            jsonA.file_key = file_key;
            formData.append(file_key, audio_file);
            audios_counter++;
        }
        jsonAudios.push(jsonA);
    }

    // Texts
    let texts = document.getElementsByName('texts');
    let jsonTexts = [];
    for (let text of texts) {
        let jsonText = {
            "id": text.querySelector('[name = id]').value,
            "element_number": text.querySelector('[name = element_number]').value,
            "language1": text.querySelector('[name = language1]').value,
            "language2": text.querySelector('[name = language2]').value
        }
        jsonTexts.push(jsonText);
    }

    // Dialogues
    let dialogues = document.getElementsByName('dialogues');
    let jsonDialogues = [];
    for (let d of dialogues) {
        let jsonD = {
            "id": d.querySelector('[name = id]').value,
            "element_number": d.querySelector('[name = element_number]').value,
            "name": d.querySelector('[name = name]').value,
            "color": d.querySelector('[name = color]').value,
            "language1": d.querySelector('[name = language1]').value,
            "language2": d.querySelector('[name = language2]').value
        }
        jsonDialogues.push(jsonD);
    }


    // Exercises
    // Repeat phrases
    let repeatPhrases = document.getElementsByName('repeatPhrases');
    let jsonRepeatPhrases = [];
    for (let r of repeatPhrases) {
        let jsonR = {
            "id": r.querySelector('[name = id]').value,
            "element_number": r.querySelector('[name = element_number]').value,
            "language1": r.querySelector('[name = language1]').value,
            "language2": r.querySelector('[name = language2]').value,
            "show_text": r.querySelector('[name = show_text]').checked
        }
        jsonRepeatPhrases.push(jsonR);
    }

    // Spellchecks
    let spellchecks = document.getElementsByName('spellchecks');
    let jsonSpellchecks = [];
    for (let s of spellchecks) {
        let jsonS = {
            "id": s.querySelector('[name = id]').value,
            "element_number": s.querySelector('[name = element_number]').value,
            "wrong_text": s.querySelector('[name = wrong_text]').value,
            "right_text": s.querySelector('[name = right_text]').value,
            "translated_right_text": s.querySelector('[name = translated_right_text]').value
        }
        jsonSpellchecks.push(jsonS);
    }

    // Multiple choice questions
    let mc_questions = document.getElementsByName('mc_questions');
    let jsonMc_questions = [];
    for (let q of mc_questions) {
        // Object for questions
        let qObj = {
            "id": q.querySelector('[name = id]').value,
            "element_number": q.querySelector('[name = element_number]').value,
            "text": q.querySelector('[name = text]').value,
            "t_text": q.querySelector('[name = t_text]').value,
            "randomize_choices": q.querySelector('[name = randomize_choices]').checked,
            "choices": []
        }
        // Object for choices
        let choices = q.querySelectorAll('.choice');
        for (let c of choices) {
            let cObj = {
                "id": c.querySelector('[name = id]').value,
                "choice_number": c.querySelector('[name = choice_number]').value,
                "text": c.querySelector('[name = text]').value,
                "t_text": c.querySelector('[name = t_text]').value,
                "correct": c.querySelector('[name = correct]').classList.contains('checked')
            }
            // Add choices to the question
            qObj.choices.push(cObj);
        }
        jsonMc_questions.push(qObj);
    }

    // Build Json to send
    let jsonData = {
        "page_id": page_id,
        "sub1": sub1 = document.getElementById('sub1').value,
        "sub2": sub2 = document.getElementById('sub2').value,
        "images": jsonImages,
        "videos": jsonVideos,
        "audios": jsonAudios,
        "texts": jsonTexts,
        "dialogues": jsonDialogues,
        "repeatPhrases": jsonRepeatPhrases,
        "spellchecks": jsonSpellchecks,
        "mc_questions": jsonMc_questions,
        "deleted": objects_deleted
    }

    formData.append("data", JSON.stringify(jsonData));

    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: URL_SAVE_PAGE,
        data: formData,
        processData: false,  // Tell jQuery not to process the data
        contentType: false,  // Tell jQuery not to set the content type
        headers: { "X-CSRFToken": csrftoken },
        success: function (response) {
            switch (response.message) {
                case "success":
                    window.location.href = URL_VIEW_PAGES;
                    break;
            }
        },
        error: function (response) {
            //console.error(response);
        }
    });
}