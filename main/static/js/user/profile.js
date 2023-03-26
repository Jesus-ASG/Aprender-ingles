let progress_lvl_dom = document.getElementById('progress_level');
let progress_lvl_value = parseInt(db_progress_xp * 100);

let progress_writing_dom = document.querySelector('#writing_average .basic-progress-level');
let progress_comprehension_dom = document.querySelector('#comprehension_average .basic-progress-level');
let progress_speaking_dom = document.querySelector('#speaking_average .basic-progress-level');

// Level progress is filled to 320°
progressAnimation(progress_lvl_dom, progress_lvl_value, 320);

progressAnimation(progress_writing_dom, db_writing_average);
progressAnimation(progress_comprehension_dom, db_comprehension_average);
progressAnimation(progress_speaking_dom, db_speaking_average);


let change_profile_picture = document.getElementById('change_profile_picture');
change_profile_picture.addEventListener('mouseenter', (e) => {
  change_profile_picture.style.opacity = '1';
});

change_profile_picture.addEventListener('mouseleave', (e) => {
  change_profile_picture.style.opacity = '0';
});

// Add event listener for select
let default_ppi = document.querySelectorAll('#change_img_form img');
default_ppi.forEach(img => {
  img.addEventListener('click', (e) => {
    default_ppi.forEach(img2 => {
      let parent2 = img2.parentElement.parentElement.parentElement;
      parent2.classList.remove('selected');
    });
    let parent = img.parentElement.parentElement.parentElement;
    parent.classList.add('selected');
  })
});;


// Default profile picture ~image element~
// 'The image who is inside a label and together a element with id=default_pp'
let default_pp_sb = document.querySelector('#default_pp ~ label img');
if (default_pp_sb)
  default_pp_sb.click();
else {
  default_pp_sb = default_ppi[2]; // 2 belongs to hungry panda
}

// Select default image every time modal is opened
document.getElementById('change_profile_picture').addEventListener('click', e => {
  default_pp_sb.click();
});



function progressAnimation(progress, end_value, fill_to) {
  let deg = 3.6;
  if (fill_to)
    deg = fill_to / 100
  let progress_value = 0;
  let speed = 20;
  //conic-gradient(#23fbb7 ${progress_value * deg}deg, #bbfff3 ${progress_value * deg}deg)
  let progress_interval = setInterval(() => {
    progress.style.background = `
      conic-gradient(#23fbb7 ${progress_value * deg}deg, #bbfff3 ${progress_value * deg}deg)
      `;
    if (progress_value == end_value)
      clearInterval(progress_interval);
    progress_value++;
  }, speed);
}