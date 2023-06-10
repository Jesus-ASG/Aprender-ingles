const currentURL = window.location.href;
// Get all the nav links
const navLinks = document.querySelectorAll('.nav-link');
// Loop through the links
navLinks.forEach(link => {
	// If the link URL matches the current URL, add the active class to it
	if (link.href === currentURL)
		link.classList.add('active');
});

/**
 * @returns a String id of o random letters
 * 'A' = 65
 * 'Z'= 90
 * 'a' = 97
 * 'z' = 122
 */
function generateStringId() {
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

function makeAdjustable(element) {
	element.style.height = (element.style.fontSize) / 2;
	element.style.height = `${element.scrollHeight}px`;

	element.addEventListener("keyup", e => {
		element.style.height = (element.style.fontSize) / 2;
		let h = e.target.scrollHeight;
		element.style.height = `${h}px`;
	});

	element.addEventListener("mousewheel", (e) => {
		if (!element.matches(':focus')) {
			e.preventDefault();
			window.scrollBy(0, e.deltaY);
		}
	});

	$(window).on("load resize", () => {
		element.style.height = `${element.scrollHeight}px`;
	});
}

function hasContent(object) {
	if (object == undefined || object == null)
		return false;
	try {
		return (Object.keys(object).length > 0)
	} catch (e) { return false; }
}