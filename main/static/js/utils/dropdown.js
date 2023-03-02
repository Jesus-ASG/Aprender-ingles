const items = document.querySelectorAll(".item");

items.forEach(item => {
    item.addEventListener("click", () => {
        item.classList.toggle("checked");
        let check_input = document.getElementById(item.getAttribute('target'));
        if (check_input)
            check_input.checked = !check_input.checked;


        let checked = document.querySelectorAll(".checked"),
            btnText = document.querySelector(".btn-text");

            if(checked && checked.length > 0){
                btnText.innerText = `${checked.length} Selected`;
            }else{
                btnText.innerText = "Select Language";
            }
    });
})
