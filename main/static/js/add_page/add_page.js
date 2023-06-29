let objects_deleted = {
    "images": [],
    "videos": [],
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
        let name = element_to_delete.getAttribute("name");
        switch (name) {
            case "images":
                objects_deleted.images.push(id_database);
                break;
            case "videos":
                objects_deleted.videos.push(id_database);
                break;
            case "texts":
                objects_deleted.texts.push(id_database);
                break;
            case "dialogues":
                objects_deleted.dialogues.push(id_database);
                break;
            case "repeatPhrases":
                objects_deleted.repeatPhrases.push(id_database);
                break;
            case "spellchecks":
                objects_deleted.spellchecks.push(id_database);
                break;
            case "mc_questions":
                objects_deleted.mc_questions.push(id_database);
                break;
            case "question_choices":
                objects_deleted.question_choices.push(id_database);
                break;
            default:
        }
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

function restoreImage() {
    $("#img_showed").attr("src", default_cover);
    $("#image").val("");
}

function changeImg(input) {
    if (input.value == "")
        restoreImage();
    if (input.files && input.files[0]) {
        let reader = new FileReader();
        reader.onload = function (e) {
            $("#img_showed").attr("src", e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}


function savePage() {
    let formData = new FormData();
    // Contents
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

    // Images
    let images = document.getElementsByName("images");
    let jsonImages = [];
    for (let i of images) {
        let jsonI = {
            "id": i.querySelector('[name = id]').value,
            "element_number": i.querySelector('[name = element_number]').value
        }
        jsonImages.push(jsonI);
        formData.append("imageFiles[]", i.querySelector('[name = image_file]').files[0]);
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