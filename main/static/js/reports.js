// Check auto update
let auto_update_local = localStorage.getItem('auto_update_reports');
let auto_update = document.getElementById('auto_update');

// Flag for see if a report is open currently
let report_open = false;

if (auto_update_local) {  // If auto update exists on local storage
  auto_update.checked = JSON.parse(auto_update_local);
}
else {
  auto_update.checked = true;
  localStorage.setItem('auto_update_reports', true);
}

auto_update.addEventListener('change', (e) => {
  // Change local storage variable
  localStorage.setItem('auto_update_reports', auto_update.checked);
});

// htmx
// handle notifications from messages
let ws_report_notifications_div = document.getElementById('ws_report_notifications_div');
ws_report_notifications_div.addEventListener('htmx:wsBeforeMessage', (e) => {

  // First case: Auto update is turned off
  if (!document.getElementById('auto_update').checked) {
    e.preventDefault();
    return;
  }

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
    // Ensure reports body container is visible
    document.getElementById('reports_table_body_container').classList.remove('d-none');
    // Hide report content container
    document.getElementById('report_content').classList.add('d-none');
    // Update variable for indicate a report is closed
    report_open = false;

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
function selectReport(event, id) {
  event.stopPropagation();
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

function changeStatusButton(type) {
  if (report_open) {
    let report_open = document.querySelector('.report-open-container');
    const csrftoken = getCookie('csrftoken');
    $.ajax({
      type: "PUT",
      url: URL_MODIFY_REPORTS_STATUS + '?status=' + type,
      data: JSON.stringify({ 'reports_ids': [report_open.getAttribute('current-report')] }),
      headers: { "X-CSRFToken": csrftoken },
      success: function (response) {
        if (response.success) {
          document.querySelector('.update-button').click();
        }
      },
      error: function (response) {
        //console.log(response);
      }
    });
  }


  let reports_selected = document.querySelectorAll('#reports_table_body .active');
  if (reports_selected.length == 0)
    return;

  let data = [];
  for (let r of reports_selected)
    data.push(r.getAttribute('report_id'));


  const csrftoken = getCookie('csrftoken');
  $.ajax({
    type: "PUT",
    url: URL_MODIFY_REPORTS_STATUS + '?status=' + type,
    data: JSON.stringify({ 'reports_ids': data }),
    headers: { "X-CSRFToken": csrftoken },
    success: function (response) {
      if (response.success) {

        let tabSelected = document.querySelector('.tab-item.active');
        let tabSelectedShowing = tabSelected.getAttribute('show');
        if (tabSelectedShowing != 'all' && tabSelectedShowing != type)
          for (let r of reports_selected)
            r.remove();
      }
    },
    error: function (response) {
      //console.log(response);
    }
  });
}

function openReport(report_id) {
  // Show and hide boxes for reports
  document.getElementById('reports_table_body_container').classList.add('d-none');
  document.getElementById('report_content').classList.remove('d-none');
  // Update variable for indicate a report is open
  report_open = true;

  const csrftoken = getCookie('csrftoken');
  $.ajax({
    type: "PUT",
    url: URL_MODIFY_REPORTS_STATUS + '?status=' + 'read',
    data: JSON.stringify({ 'reports_ids': [report_id] }),
    headers: { "X-CSRFToken": csrftoken },
    success: function (response) {
      if (response.success) {
        const wff = new Event('wait-for-function');
        let newUrl = URL_GET_REPORT.replace('0', report_id);

        document.querySelector(`[hx-get="${newUrl}"]`).dispatchEvent(wff);
      }
    },
    error: function (response) {
      //console.log(response);
    }
  });

}


// Handle update manual

let update_btn = document.querySelector('.update-button');

update_btn.addEventListener('click', () => {
  if (report_open) { // Update content for the report open
    let current_report_id = document.querySelector('.report-open-container').getAttribute('current-report');
    let current_row_report = document.getElementById('report_' + current_report_id);

    const wff = new Event('wait-for-function');
    let newUrl = URL_GET_REPORT.replace('0', current_report_id);

    document.querySelector(`[hx-get="${newUrl}"]`).dispatchEvent(wff);

  }
  else { // Update content for report's table
    document.querySelector('.tab-item.active').click();
  }


});