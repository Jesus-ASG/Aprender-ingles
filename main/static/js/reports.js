// htmx
// handle notifications from messages
let ws_report_notifications_div = document.getElementById('ws_report_notifications_div');
ws_report_notifications_div.addEventListener('htmx:wsBeforeMessage', (e) => {

  // First case: Auto update is false
  let autoUpdate = true;

  if (!autoUpdate)
    e.preventDefault();

  // Second case: check if is inside of unread or all messages to see changes.
  else {
    let tabSelected = document.querySelector('.tab-item.active');
    let tabSelectedShowing = tabSelected.getAttribute('show');
    if (tabSelectedShowing != 'all' && tabSelectedShowing != 'unread')
      e.preventDefault();
  }
});


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


function deleteReportsButton() {
  let reports_selected = document.querySelectorAll('#reports_table_body .active');
  if (reports_selected.length == 0)
    return;

  let data = [];
  for (let r of reports_selected)
    data.push(r.getAttribute('report_id'));


  const csrftoken = getCookie('csrftoken');
  $.ajax({
    type: "DELETE",
    url: URL_DELETE_REPORTS,
    data: JSON.stringify({ 'delete': data }),
    headers: { "X-CSRFToken": csrftoken },
    success: function (response) {
      if (response.success) {
        for (let r of reports_selected)
          r.remove();
      }
    },
    error: function (response) {
      //console.log(response);
    }
  });
}