let f_counter = { "start": 0, "end": 0 };

document.getElementById('page_title').innerHTML = createFlipHTML('Profile', 'Perfil', f_counter);

setFunctionality(f_counter);

let progress_lvl_dom = document.getElementById('progress_level');
let progress_value = 0;
let progress_end_value = parseInt(db_progress_xp * 100);
let speed = 20;


let progress_lvl = setInterval(() => {
  progress_lvl_dom.style.background = `
    conic-gradient(#23fbb7 ${progress_value * 3.2}deg, #bbfff3 ${progress_value * 3.2}deg)
    `;
  if (progress_value == progress_end_value)
    clearInterval(progress_lvl);
  progress_value++;
}, speed);


let profile_image = document.getElementById('profile_image');
profile_image.addEventListener('mouseenter', (e) => {
  let change_image_btn = document.getElementById('change_profile_picture');
  change_image_btn.style.opacity = '1';
  change_image_btn.style.visibility = 'visible';
});

let change_image_btn = document.getElementById('change_profile_picture');
change_image_btn.addEventListener('mouseleave', (e) => {
  change_image_btn.style.opacity = '0';
  change_image_btn.style.visibility = 'hidden';
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