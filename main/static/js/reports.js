// htmx
let tab_items = document.querySelectorAll('.report-tab-nav .tab-item');

tab_items.forEach(tab_item => {
  tab_item.addEventListener('click', (e) => {
    //let tool_items = document.querySelectorAll('.report-tab-nav .tab-item');
    tab_items.forEach(item => {
      item.classList.remove('active');
    });
    tab_item.classList.add('active');
  });
});


document.addEventListener('DOMContentLoaded', function () {
  document.getElementById('get_all_btn').click();
});

// On report selected
function selectReport(id) {
  let row = document.getElementById('report_' + id);
  if (row.classList.contains('active')) {
    row.classList.remove('active')
  }
  else {
    row.classList.add('active');
  }
}

function openDeleteModal() {
  let reports_selected = document.querySelectorAll('#reports_table_body .active');
  if (reports_selected.length == 0)
    return;
  document.getElementById('delete_text_info').innerText = 'Se eliminarán ' + reports_selected.length + ' reporte(s)';
  document.getElementById('open_delete_modal_button').click();
}