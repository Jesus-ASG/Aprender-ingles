let max_elem = 0;
let objects_deleted = {
    "dialogues": [],
    "repeatPhrases": []
};

// Generic functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');
		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
			cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
			break;
			}
		}
    }
    return cookieValue;
}

function deleteElement(id) {
    let element_to_delete = document.getElementById("element_"+id);
    let id_database = element_to_delete.querySelectorAll('[name = id]')[0].value
    if (id_database){
        let name = element_to_delete.getAttribute("name");
        switch(name){
            case "dialogues":
                objects_deleted.dialogues.push(id_database);
                break;
            case "repeatPhrases":
                objects_deleted.repeatPhrases.push(id_database);
                break;
            default:
        }
    }
    
    element_to_delete.remove();
    
    let html =
      `
    <div class="alert alert-success alert-dismissible fade show mb-2 mt-2" role="alert">
        <div style="text-align: center;">
            <strong>Elemento eliminado correctamente</strong>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    </div>
    `;
    document.getElementById("alert_removed_success").innerHTML = html;

    console.log(objects_deleted);
}

function restoreImage() {
    $("#img_showed").attr("src", DEFAULT_COVER);
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
    var formData = new FormData();
	// Contents
	// Dialogues
    let dialogues = document.getElementsByName('dialogues');
    let jsonDialogues = [];
    for (let i = 0; i < dialogues.length; i++) {
        let d = {
            "id": dialogues[i].querySelectorAll('[name = id]')[0].value,
            "element_number": dialogues[i].querySelectorAll('[name = element_number]')[0].value,
            "name": dialogues[i].querySelectorAll('[name = name]')[0].value,
            "color": dialogues[i].querySelectorAll('[name = color]')[0].value,
            "language1": dialogues[i].querySelectorAll('[name = language1]')[0].value,
            "language2": dialogues[i].querySelectorAll('[name = language2]')[0].value
        }
        jsonDialogues.push(d);
    }

	// Images
    let images = document.getElementsByName("images");
    let imageData = [];
    for (let i = 0; i < images.length; i++) {
        let img = {
            "id": images[i].querySelectorAll('[name = id]')[0].value,
            "element_number": images[i].querySelectorAll('[name = element_number]')[0].value
        }
        imageData.push(img);
        formData.append("imageFiles[]", images[i].querySelectorAll('[name = image]')[0].files[0]);
    }


	// Exercises
	// Repeat phrases
	let repatPhrases = document.getElementsByName('repeatPhrases');
	let jsonRepeatPhrases = [];
	for (let i = 0; i < repatPhrases.length; i++) {
        let rp = {
            "id": repatPhrases[i].querySelectorAll('[name = id]')[0].value,
            "element_number": repatPhrases[i].querySelectorAll('[name = element_number]')[0].value,
            "language1": repatPhrases[i].querySelectorAll('[name = language1]')[0].value,
            "language2": repatPhrases[i].querySelectorAll('[name = language2]')[0].value
        }
        jsonRepeatPhrases.push(rp);
    }


	// Build Json to send
    let jsonData = {
        "page_id": page_id,
        "sub1": sub1 = document.getElementById('sub1').value,
        "sub2": sub2 = document.getElementById('sub2').value,
        "dialogues": jsonDialogues,
		"repeatPhrases": jsonRepeatPhrases,
        "imageData": imageData,
        "deleted": objects_deleted
    }

    formData.append("data", JSON.stringify(jsonData));
    /*
    formData.forEach((value, key) => {
      console.log(key, value);
    });
    */
    
    const csrftoken = getCookie('csrftoken');
    $.ajax({
        type: "POST",
        url: "/myadmin/add-page/"+story_route+"/"+page_type,
        data: formData,
        processData: false,  // Tell jQuery not to process the data
        contentType: false,  // Tell jQuery not to set the content type
        headers: { "X-CSRFToken": csrftoken },
        success: function (response) {
            //console.log(response);
        }
    });
}