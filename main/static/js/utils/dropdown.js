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
					if (item.classList.contains("checked")) {
						for (let i of items)
							if (i.classList.contains("checked")) {
								clickCheckbox(i);
							};
					} else {
						for (let i of items)
							if (!i.classList.contains("checked")) {
								clickCheckbox(i);
							};
					}
					showLabelMessage(menu_items);
				});
			}
		} else {
			item.addEventListener("click", () => {
				let input = item.querySelector("input");
				if (input) {
					let input_type = input.getAttribute("type");

					switch (input_type) {
						case "checkbox":
							clickCheckbox(item);
							showLabelMessage(menu_items);
							if (dom_select_all) {
								let checked = menu_items.querySelectorAll(".checked");
								if (checked.length < items.length) {
									if (checked.length == items.length - 1 && !dom_select_all.classList.contains("checked")) {
										dom_select_all.classList.add("checked");
										let check_input = document.getElementById(item.getAttribute("target"));
										if (check_input)
											check_input.checked = true;
									}
									else {
										dom_select_all.classList.remove("checked");
										let check_input = document.getElementById(item.getAttribute("target"));
										if (check_input)
											check_input.checked = false;
									}
								}
							}
							break;

						case "radio":
							console.log("is radio");
					}
				}
			});
		}
	}
}

/*
function clearSelection(item){
		item.classList.remove('checked');
		let check_input = 
}
*/

function clickCheckbox(item) {
	item.classList.toggle("checked");
	let check_input = document.getElementById(item.getAttribute("target"));
	if (check_input)
		check_input.checked = !check_input.checked;
}

function showLabelMessage(menu_items) {
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
