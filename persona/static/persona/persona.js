var authCode;

$(function() {
  parseQuery();
});

function parseQuery() {
  var currentQuery = new URLSearchParams(window.location.search);
  authCode = currentQuery.get("code");

  var params = "{'code': authCode}";
  var xhttp = new XMLHTTPRequest();

  xhttp.setRequestHeader('Content-type', 'application/json');
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("ya").innerHTML = xhttp.responseText;
  };

  xhttp.open("POST", "http://127.0.0.1:8000/persona/app/", true);
  xhttp.send(params);
  //$.post("http://127.0.0.1:8000/persona/app", {'code': authCode}, analyzeProfile);
}

function analyzeProfile(data) {

  $( "#ya" ).append(data[0]);
  return 0;

}
