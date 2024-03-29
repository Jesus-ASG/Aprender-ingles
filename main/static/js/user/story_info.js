function setTitle(f_counter) {
    let domTitle = document.getElementById("story_title");
    if (domTitle != null && domTitle!= undefined)
        domTitle.innerHTML = createFlipHTML(db_title.title1, db_title.title2, f_counter);
}


function loadLikes() {
    let btn = document.getElementById("like_counter_btn").children[0];
    let lbl = document.getElementById("like_counter_lbl");

    if (db_story_liked)
        btn.classList.add("fas");
    else
        btn.classList.add("far");

    lbl.innerText = db_story_likes_number;
}

function likeFunction(e) {
    let lbl = document.getElementById("like_counter_lbl");
    try {
        let likes = parseInt(lbl.textContent);
        if (db_story_liked) likes--;
        else likes++;

        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: URL_LIKE_STORY,
            headers: { "X-CSRFToken": csrftoken },
            success: function (response) {
                //console.log(response);
            },
            error: function (response) {
                //console.log(response);
            }
        });

        lbl.innerText = likes;
        e.target.classList.toggle("far");
        e.target.classList.toggle("fas");
        db_story_liked = !db_story_liked;
    } catch (error) { }
}


function loadSaved() {
    let btn = document.getElementById("save_story_btn").children[0];
    let lbl = document.getElementById("save_story_lbl");
    if (db_story_saved) {
        lbl.innerText = 'Saved';
        btn.classList.toggle("fas");
    }
    else {
        lbl.innerText = 'Save';
        btn.classList.toggle("far");
    }
}

function saveFunction(e) {
    let lbl = document.getElementById("save_story_lbl");
    try {
        const csrftoken = getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: URL_SAVE_STORY,
            headers: { "X-CSRFToken": csrftoken },
            success: function (response) {
                //console.log(response);
            },
            error: function (response) {
                //console.log(response);
            }
        });

        db_story_saved = !db_story_saved;

        if (db_story_saved)
            lbl.innerText = 'Saved';
        else
            lbl.innerText = 'Save';

        e.target.classList.toggle("far");
        e.target.classList.toggle("fas");
    } catch (error) { }
}


function setStatisticsLabels(f_counter) {
    let results_dom = document.getElementById("results");
    let score_lbl1 = `Best score`;
    let score_lbl2 = `Mejor puntaje`;

    let comprehension = results_dom.querySelector("[name = comprehension]");
    let writing = results_dom.querySelector("[name = writing]");
    let speaking = results_dom.querySelector("[name = speaking]");

    // Titles
    results_dom.querySelector("[name = title_score]").innerHTML = createFlipHTML(score_lbl1, score_lbl2, f_counter);
    comprehension.querySelector("[name = title]").innerHTML = createFlipHTML("Comprehension", "Comprensión", f_counter);
    writing.querySelector("[name = title]").innerHTML = createFlipHTML("Writing", "Escritura", f_counter);
    speaking.querySelector("[name = title]").innerHTML = createFlipHTML("Speaking", "Pronunciación", f_counter);
}

function setScoresLabels(f_counter) {
    let table_scores = document.getElementById("scores_table");
    let table_no_scores = table_scores.querySelector("[name = no_scores]");
    let table_header = table_scores.querySelector("[name = table_header]");

    table_scores.querySelector("[name = title]").innerHTML = createFlipHTML("Scores table", "Tabla de puntuaciones", f_counter);

    if (table_no_scores)
        table_no_scores.innerHTML = createFlipHTML("No records yet", "Aún no hay registros", f_counter);

    if (table_header) {
        let html = `
        <th scope="col" class="fs-4">`+ createFlipHTML("Position", "Posición", f_counter) + `</th>
        <th scope="col" class="fs-4">`+ createFlipHTML("Score", "Puntaje", f_counter) + `</th>
        <th scope="col" class="fs-4">`+ createFlipHTML("Date", "Fecha", f_counter) + `</th>
        `;
        table_header.innerHTML = html;
    }
}

function setRelatedTitle(f_counter) {
    let related_title = document.getElementById("related_title");
    if (related_title!=null && related_title!=undefined)
        related_title.innerHTML = createFlipHTML("Related", "Relacionado", f_counter);
}

function deleteAnswers() {
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: URL_DELETE_ANSWERS,
        headers: { "X-CSRFToken": csrftoken },
        success: function (response) {
            if (response.message == 'success') {
                document.getElementById('start_answer_story').click();
            }
        },
        error: function (response) { }
    });

}