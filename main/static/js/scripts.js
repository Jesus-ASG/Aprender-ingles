function makeAdjustable(element) {
  element.style.height = (element.style.fontSize) / 2;

  element.style.height = `${element.scrollHeight}px`;
  element.addEventListener("keydown", e => {
    element.style.height = (element.style.fontSize) / 2;
    let h = e.target.scrollHeight;
    element.style.height = `${h}px`;
  });
}