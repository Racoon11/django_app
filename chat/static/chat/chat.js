

var csrf;
var input_test;
var scroll;
function chat(csrftoken) {
    csrf = csrftoken;
    input_test = document.getElementById("inputMessage");
    scroll = document.getElementById("scroll");

    var form = document.getElementById("my-form");
    function handleForm(event) { event.preventDefault(); }
    form.addEventListener('submit', handleForm);
}
function send_message() {
    let text = input_test.value;
    input_test.value = "";
    show_message(text, "me")
    fetch("/chat/get_answer", {
      method: "POST",
      body: JSON.stringify({
        "message": text
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
        'X-CSRFToken': csrftoken
      }
    }).then(response => response.json())
  .then(response => show_message(response['ans'], "opponent"));
}

function show_message(resp, whose) {
    console.log(resp);
    div1 = document.createElement("div");
    div1.className = "row d-flex " + (whose === "me" ? "justify-content-end" : "justify-content-start");
    div2 = document.createElement("div");
    div2.className = whose + " col-md-8 border border-3 rounded-4 " + (whose === "me" ? "border-primary " : "border-secondary");
    p = document.createElement("p");
    p.className = whose === "me" ? "text-end" : "";
    p.textContent = resp;
    div2.appendChild(p);
    div1.appendChild(div2);
    scroll.appendChild(div1);

    scroll.scrollTop = scroll.scrollHeight;
}
