function setTitle(f_counter) {
    let f_classes = {
        "paper": "mx-1",
        "front": "px-1",
        "back": "px-1"
    };
    document.getElementById("story_title").innerHTML = createFlipHTML(db_title.title1, db_title.title2, f_counter, f_classes);
}

function setStatisticsLabels(f_counter) {
    let f_classes = {
        "paper": "mx-1",
        "front": "px-1",
        "back": "px-1"
    };
    let results_dom = document.getElementById("results");
    let score_lbl1 = `High score: ${db_high_score}pts`;
    let score_lbl2 = `Puntuación más alta: ${db_high_score}pts`;

    let comprehension = results_dom.querySelector("[name = comprehension]");
    let writing = results_dom.querySelector("[name = writing]");
    let speaking = results_dom.querySelector("[name = speaking]");

    // Titles
    results_dom.querySelector("[name = title_score]").innerHTML = createFlipHTML(score_lbl1, score_lbl2, f_counter, f_classes);
    comprehension.querySelector("[name = title]").innerHTML = createFlipHTML("Comprehension", "Comprensión", f_counter, f_classes);
    writing.querySelector("[name = title]").innerHTML = createFlipHTML("Writing", "Escritura", f_counter, f_classes);
    speaking.querySelector("[name = title]").innerHTML = createFlipHTML("Speaking", "Pronunciación", f_counter, f_classes);
}

function setScoresLabels(f_counter) {
    let f_classes = {
        "paper": "mx-1",
        "front": "px-1",
        "back": "px-1"
    };
    let table_scores = document.getElementById("scores_table");
    table_scores.querySelector("[name = title]").innerHTML = createFlipHTML("Scores table", "Tabla de puntuaciones", f_counter, f_classes);
    table_scores.querySelector("[name = no_scores]").innerHTML = createFlipHTML("No records yet", "Aún no hay registros", f_counter, f_classes);

    let html = `
    <th scope="col" class="fs-4">`+ createFlipHTML("Position", "Posición", f_counter, f_classes) + `</th>
    <th scope="col" class="fs-4">`+ createFlipHTML("Score", "Puntaje", f_counter, f_classes) + `</th>
    <th scope="col" class="fs-4">`+ createFlipHTML("Date", "Fecha", f_counter, f_classes) + `</th>
    `;
    table_scores.querySelector("[name = table_header]").innerHTML = html;
}

function cleanStorage() {
    localStorage.removeItem('story_answers_' + db_story_id);
}