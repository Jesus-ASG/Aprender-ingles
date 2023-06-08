/**
 * @returns a String id of o random letters
 * 'A' = 65
 * 'Z'= 90
 * 'a' = 97
 * 'z' = 122
 */
function generateId() {
	id = "";
	for (let i = 0; i < 8; i++) {
		num = Math.floor(Math.random() * 52);
		if (num <= 25)
			num += 65;
		else
			num += 71;
		id += String.fromCharCode(num);
	}
	return id;
}
/*
	Example of use
	<div id="flip_text">
		<p class="front">This text goes to front</p>
		<p class="back">This text goes to back</p>
	</div>
	document.getElementById('flip_text').flipText();
*/
HTMLElement.prototype.flipText = function (e) {
	front = this.querySelector('.front');
	back = this.querySelector('.back');

	if (front === null || back === null)
		return;

	// Classes
	front_classes = front.classList.value + "";
	back_classes = back.classList.value + "";

	front_classes = front_classes.replace('front ', '');
	back_classes = back_classes.replace('back ', '');

	// Text
	text1 = front.innerText;
	text2 = back.innerText;

	let arr1 = text1.split("|");
	let arr2 = text2.split("|");

	// Html
	let html = ``;
	let flip_ids = [];
	for (let i = 0; i < arr1.length; i++) {
		// Id
		paper_id = generateId();

		let words1 = arr1[i].replace(/ {2,}/g, ' ').trim(); // removes extra spaces
		let words2 = arr2[i].replace(/ {2,}/g, ' ').trim(); // removes extra spaces

		words1 = words1.split(" ");
		words2 = words2.split(" ");

		let max = words1.length > words2.length ? words1.length : words2.length;
		for (let j = 0; j < max; j++) {
			let has_content = true;
			try {
				if (words1[j] == '' || words1[j] == '')
					has_content = false;
			} catch (e) { }

			if (!has_content)
				continue;

			html += `<div class="paper paper_${paper_id}">`;

			if ((j < words1.length) && (j < words2.length)) {
				if (j < words1.length)
					html += `<div class="front ${front_classes}"> ${words1[j]} </div>`;

				if (j < words2.length)
					html += `<div class="back p-abs ${back_classes}"> ${words2[j]} </div>`;
			}
			else {
				if (j < words1.length)
					html += `<div class="front extra ${front_classes}"> ${words1[j]} </div>`;
				else if (j >= words1.length)
					html += `<div class="front extra" style="border:none;color:rgba(0,0,0,0);background:rgba(0,0,0,0);width=0;"></div>`;

				if (j < words2.length)
					html += `<div class="back extra hide-extras p-abs ${back_classes}"> ${words2[j]} </div>`;
				else if (j >= words2.length)
					html += `<div class="back extra hide-extras p-abs px-1" style="border:none;color:rgba(0,0,0,0);background:rgba(0,0,0,0);"></div>`;
			}
			html += `</div>`;
			let flag = false;
			try {
				if (words1[j].includes("<span></span>"))
					flag = true;
			} catch (e) { }

			try {
				if (words2[j].includes("<span></span>"))
					flag = true;
			} catch (e) { }

			if (flag)
				html += `<br>`;
		}
		flip_ids.push(paper_id);
	}

	this.innerHTML = html;
	for (let id of flip_ids)
		flipPapers(id);

}

function flipPapers(id) {

	let papers = document.getElementsByClassName("paper_" + id);

	for (let paper of papers) {
		paper.addEventListener("click", () => {
			let fronts = document.querySelectorAll(".paper_" + id + " .front");
			let backs = document.querySelectorAll(".paper_" + id + " .back");
			let ex = document.querySelectorAll(".paper_" + id + " .extra");

			for (let e of ex)
				e.classList.toggle("hide-extras");

			for (let f of fronts)
				f.classList.toggle("p-abs");

			for (let b of backs)
				b.classList.toggle("p-abs");

			for (let paper2 of papers)
				paper2.classList.toggle("flip");
		});

		paper.addEventListener("mouseenter", () => {
			let fronts = document.querySelectorAll(".paper_" + id + " .front");
			let backs = document.querySelectorAll(".paper_" + id + " .back");
			for (let f of fronts)
				f.classList.add("color-hover");
			for (let b of backs)
				b.classList.add("color-hover");
		});

		paper.addEventListener("mouseleave", () => {
			let fronts = document.querySelectorAll(".paper_" + id + " .front");
			let backs = document.querySelectorAll(".paper_" + id + " .back");
			for (let f of fronts)
				f.classList.remove("color-hover");
			for (let b of backs)
				b.classList.remove("color-hover");
		});
	}
}
