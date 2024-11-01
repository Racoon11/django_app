

var word_trans = {};
var word_id = {};
var csrftoken;
function show_list(words, trans, ids, csrf) {
    words = words.split('&#x27;');
    trans = trans.split('&#x27;');
    ids = ids.split('&#x27;')
    csrftoken = csrf;

    for (var i=1; i < words.length; i+=2) {
        word_trans[words[i]] = trans[i];
        word_id[words[i]] = ids[i];
    }

    var div_main = document.getElementById("div-last");
    for (const [key, value] of Object.entries(word_trans)) {
        var form = document.createElement("form");
        form.className = "row g-3";
        form.addEventListener('submit', handleForm);

        var div1 = document.createElement("div");
        div1.className = "col-auto";

        var inp_eng = document.createElement("input");
        inp_eng.type="text";
        inp_eng.value = key;
        inp_eng.className = "form-control word-change";
        inp_eng.setAttribute("disabled", "disabled");
        inp_eng.id = "eng-" + word_id[key];

        div1.appendChild(inp_eng);
        form.appendChild(div1);

        var div2 = document.createElement("div");
        div2.className = "col-auto";
        div2.textContent = " - ";
        form.appendChild(div2);

        var div3 = document.createElement("div");
        div3.className = "col-auto";

        var inp_rus = document.createElement("input");
        inp_rus.type="text";
        inp_rus.value = value;
        inp_rus.className = "form-control word-change";
        inp_rus.setAttribute("disabled", "disabled");
        inp_rus.id = "rus-" + word_id[key];

        div3.appendChild(inp_rus);
        form.appendChild(div3);

        var div4 = document.createElement("div");
        div4.className = "col-auto";

        var del_btn = document.createElement("button");
        del_btn.className = "btn btn-danger";
        del_btn.textContent = "delete";
        del_btn.value = word_id[key];
        del_btn.onclick = delete_word.bind(this);
        div4.appendChild(del_btn);
        form.appendChild(div4);

        var div5 = document.createElement("div");
        div5.className = "col-auto";

        var add_btn = document.createElement("button");
        add_btn.className = "btn btn-success";
        add_btn.textContent = "add";
        add_btn.onclick = add_word.bind(this);
        add_btn.value = word_id[key];
        div5.appendChild(add_btn);
        form.appendChild(div5);

        var div6 = document.createElement("div");
        div6.className = "col-auto";

        var chg_btn = document.createElement("button");
        chg_btn.className = "btn btn-primary";
        chg_btn.textContent = "change";
        chg_btn.value = word_id[key];
        chg_btn.onclick = change_word.bind(this);
        div6.appendChild(chg_btn);
        form.appendChild(div6);

        div_main.appendChild(form);
        div_main.appendChild(document.createElement("br"));
    }
}

function delete_word(btn) {
    fetch("/keywords/admin", {
      method: "POST",
      body: JSON.stringify({
        "operation": "delete",
        "word_id": btn.target.value
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
        'X-CSRFToken': csrftoken
      }
    }).then((response) => location.reload());
}

function add_word(btn) {
    var vl = btn.target.value;
    var rus = document.getElementById("rus-"+vl);
    var eng = document.getElementById("eng-"+vl);
    let word_eng = eng.value;
    let word_rus = rus.value;
    fetch("/keywords/admin", {
      method: "POST",
      body: JSON.stringify({
        "operation": "add",
        "word_id": btn.target.value,
        "word_eng": word_eng,
        "word_rus": word_rus
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
        'X-CSRFToken': csrftoken
      }
    }).then((response) => location.reload());
}

function change_word(btn) {
    var vl = btn.target.value;
    var rus = document.getElementById("rus-"+vl);
    var eng = document.getElementById("eng-"+vl);
    rus.disabled = false;
    eng.disabled = false;
}
function handleForm(event) { event.preventDefault(); }
