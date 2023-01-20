let total_translations = 0;

for (let dialogue of db_dialogues) {
	
	//let text1 = dialogue.content1;
	//let text2 = dialogue.content2;
	let text1 = dialogue.content1.replace(/\n/g, '<span></span>|');
	let text2 = dialogue.content2.replace(/\n/g, '<span></span>|');
	// Create html
	let arr1 = text1.split("|");
	let arr2 = text2.split("|");

	let html = `<div class="row" style="color:rgba(0,0,0,0)"><br></div>
	<div class="fw-bold fs-5 dialogue-name" style="color:`+dialogue.color+`;">
	<p>`+dialogue.name+`:</p></div>`;
	for (let i = 0; i <arr1.length; i++) {
		let words1 = arr1[i].replace(/ {2,}/g, ' ').trim(); // removes extra spaces
		//let words2 = arr2[i].replace(/\s+/g, ' ').trim(); // removes extra spaces
		let words2 = arr2[i].replace(/ {2,}/g, ' ').trim();
		
		words1 = words1.split(" ");
		words2 = words2.split(" ");

		let max = words1.length > words2.length ? words1.length : words2.length;
		for (let j = 0; j < max; j++) {
			html += `<div class="paper paper_` + total_translations + ` mx-1 fw-bold fs-5">`;

			if ((j < words1.length) && (j < words2.length)) {
				if (j < words1.length)
					html += `<div class="front styles-front">` + words1[j] + `</div>`;

				if (j < words2.length)
					html += `<div class="back p-abs styles-back">` + words2[j] + `</div>`;
			}
			else {
				if (j < words1.length)
					html += `<div class="front extra styles-front">` + words1[j] + `</div>`;
				else if (j >= words1.length)
					html += `<div class="front extra" style="border:none;color:rgba(0,0,0,0);background:rgba(0,0,0,0);width=0;"></div>`;

				if (j < words2.length)
					html += `<div class="back extra hide-extras p-abs styles-back">` + words2[j] + `</div>`;
				else if (j >= words2.length)
					html += `<div class="back extra hide-extras p-abs" style="border:none;color:rgba(0,0,0,0);background:rgba(0,0,0,0);"></div>`;
			}
			html += `</div>`;
			let flag = false;
			try{
				if (words1[j].includes("<span></span>"))
					flag = true;
			} catch (e){}

			try{
				if (words2[j].includes("<span></span>"))
					flag = true;
			} catch (e){}

			if (flag)
				html += `<br>`;
			
		}
		total_translations++;
	}
	html += `<div id="dialogues_area"></div>`;
	document.getElementById("dialogues_area").outerHTML = html;


}

setFunctionality();


function setFunctionality(){
	for (let i = 0; i < total_translations; i++) {
		let papers = document.getElementsByClassName("paper_" + i);
	
		for (let paper of papers) {
			paper.addEventListener("click", () => {
				let fronts = document.querySelectorAll(".paper_" + i + " .front");
				let backs = document.querySelectorAll(".paper_" + i + " .back");
				let ex = document.querySelectorAll(".paper_" + i + " .extra");
	
				for (let e of ex)
					e.classList.toggle("hide-extras");
				
				for (let f of fronts) 
					f.classList.toggle("p-abs");
	
				for (let b of backs) 
					b.classList.toggle("p-abs");
	
				for (let paper2 of papers)
					paper2.classList.toggle("flip");
			});

			paper.addEventListener("mouseenter", () =>{
				let fronts = document.querySelectorAll(".paper_" + i + " .front");
				let backs = document.querySelectorAll(".paper_" + i + " .back");
				for (let f of fronts) 
					f.classList.add("color-hover");
				for (let b of backs) 
					b.classList.add("color-hover");
			});

			paper.addEventListener("mouseleave", () =>{
				let fronts = document.querySelectorAll(".paper_" + i + " .front");
				let backs = document.querySelectorAll(".paper_" + i + " .back");
				for (let f of fronts) 
					f.classList.remove("color-hover");
				for (let b of backs) 
					b.classList.remove("color-hover");
			});
		}
	}
}
