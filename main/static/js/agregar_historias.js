txt_historias = document.getElementById("txt_historias");
txt_historias.value = "";

txt_historias.addEventListener("keyup", e =>{
    txt_historias.style.height = "60px";
    let scHeight = e.target.scrollHeight;
    txt_historias.style.height = `${scHeight}px`;
});