function clearSearchInput() {
	let input = document.getElementById('search_input');
	input.value = '';
	input.focus();
}


const menu_items_list = document.getElementsByClassName("menu-items");

for (let menu_items of menu_items_list) {
	let items = menu_items.getElementsByClassName("item");
	let dom_select_all = null;

	for (let item of items) {
		let x = item.getAttribute("select-all");
		if (x == "true") {
			dom_select_all = item;

			let select_all = item.getAttribute("select-all");
			if (select_all == "true") {

				item.addEventListener("click", () => {
					let input = item.querySelector('input');

					if (item.classList.contains("checked")) {
						for (let i of items) {
							input.checked = false;
							i.classList.remove("checked");
							let input_i = i.querySelector('input');
							input_i.checked = false;
						}
					}
					else {
						for (let i of items) {
							input.checked = true;
							i.classList.add("checked");
							let input_i = i.querySelector('input');
							input_i.checked = true;
						}

					}
					showCheckboxLabel(menu_items);
				});
			}
		}
		else {
			item.addEventListener("click", () => {
				let input = item.querySelector("input");
				if (input) {
					let input_type = input.getAttribute("type");
					switch (input_type) {
						case "checkbox":
							item.classList.toggle("checked");
							input.checked = !input.checked;

							if (dom_select_all) {
								let checked = menu_items.querySelectorAll(".checked");

								// All is checked
								if (dom_select_all.classList.contains("checked")) {
									// But it should'nt -> quit checked state
									if (checked.length < items.length) {
										dom_select_all.classList.remove("checked");
										let input_all = dom_select_all.querySelector('input');
										input_all.checked = false;
									}
								}
								// All is no checked
								else {
									// But it should do
									if (checked.length == items.length - 1) {
										dom_select_all.classList.add("checked");
										let input_all = dom_select_all.querySelector('input');
										input_all.checked = true;
									}
								}
							}

							showCheckboxLabel(menu_items);
							break;

						case "radio":
							for (let i of items)
								i.classList.remove('checked');

							item.classList.add('checked');
							input.checked = true;

							showRadioLabel(menu_items);
							break;
					}
				}
			});
		}
	}
}

function showCheckboxLabel(menu_items) {
	let checked = menu_items.querySelectorAll(".checked");
	const label_id = menu_items.getAttribute("label-id");
	const default_label = menu_items.getAttribute("default-label");

	if (label_id && default_label) {
		let label = document.getElementById(label_id);
		if (label) {
			if (checked && checked.length > 0) {
				label.innerText = `${checked.length} Selected`;
			} else {
				label.innerText = default_label + "";
			}
		}
	}
}

function showRadioLabel(menu_items) {
	const label_id = menu_items.getAttribute("label-id");
	const default_label = menu_items.getAttribute("default-label");
	if (label_id && default_label) {
		const label = document.getElementById(label_id);

		let text = menu_items.querySelector('.checked > .item-text').textContent || '';

		if (label && label_id) {
			if (text.toLowerCase() == 'default')
				label.innerText = default_label + "";
			else
				label.innerText = text;
		}
	}
}


// Init checkbox and radio
for (let menu_items of menu_items_list) {
	let items = menu_items.getElementsByClassName("item");
	for (let item of items) {
		let input = item.querySelectorAll('input');
		input.forEach(input => {
			if (input.checked)
				item.classList.add('checked');
		});
	}
	let type = menu_items.querySelector('input').type;
	switch (type) {
		case 'checkbox':
			showCheckboxLabel(menu_items);
			break;
		case 'radio':
			showRadioLabel(menu_items);
			break;
	}
}

// Sort by name
/*
let sort_by_name = document.getElementById('sort_by_name');
let sort_by_name_icon = sort_by_name.querySelector('i');
let sort_by_name_input = sort_by_name.querySelector('input');

sort_by_name.addEventListener('click', (e) => {
	let value = sort_by_name_input.value;
	if (value == 'default')
		sort_by_name_input.value = 'z-a';
	else
		sort_by_name_input.value = 'default';

	sort_by_name_icon.classList.toggle('fa-arrow-down-a-z');
	sort_by_name_icon.classList.toggle('fa-arrow-down-z-a');

});
*/
