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

	element.addEventListener("mousewheel", (e)=>{
		if (!element.matches(':focus')) {
			e.preventDefault();
			window.scrollBy(0, e.deltaY);
		}
	});

	$(window).on("load resize", () => {
		element.style.height = `${element.scrollHeight}px`;
	});
}