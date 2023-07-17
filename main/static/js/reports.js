reportTemplateSocket = new WebSocket(`ws://${window.location.host}/ws/report-notifications/`);


reportTemplateSocket.onmessage = function (e) {
  console.log('manage reports template');
  console.log(e);

}