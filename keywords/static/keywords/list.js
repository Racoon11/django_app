

var word_status = {};
var word_trans = {};
var word_id = {};
function show_list(words, trans, ids, csrftoken) {
    words = words.split('&#x27;');
    trans = trans.split('&#x27;');
    ids = ids.split('&#x27;');

    for (var i=1; i < words.length; i+=4) {
        word_status[words[i]] = words[i+2];
        word_trans[trans[i]] = trans[i+2];
        word_id[ids[i]] = ids[i+2];
    }

    var ul = document.getElementById("list");
    var i = 0;
    for (const [key, value] of Object.entries(word_status)) {
        var li = document.createElement('li');
        li.className = "list-group-item";

        var div1 = document.createElement("div");
        div1.className = "ms-2 me-auto";

        var div2 = document.createElement("div");
        div2.className = "";
        var p1 = document.createElement("label");

        if (word_trans[key] == "none") {
            p1.textContent = key;
        } else {
            p1.textContent = key + " - " + word_trans[key];
        }
        p1.setAttribute("for", i);

        var inp = document.createElement("input");
        inp.className = "form-check-input me-1";
        inp.setAttribute("type", "checkbox");
        inp.name = i;
        inp.id = i;
        inp.value = word_id[key];
        i++;
        var p2 = document.createElement("p");
        switch (value) {
            case "base": {
                break;
            }
            case "user": {
                inp.setAttribute("checked", "checked");
                inp.disabled = "disabled";
                p2.textContent = "You already have this word in your dictionary";

                break;
            }
            case "check": {
                inp.disabled = "disabled";

                p2.textContent = "We do not have this word in our base, but we have sent it to our moderator to check it";
                //div1.appendChild(p2);
                break;
            }
        }

        div2.appendChild(inp);
        div2.appendChild(p1);
        //div2.textContent = key;
        div1.appendChild(div2);
        div1.appendChild(p2);
        li.appendChild(div1);
        ul.appendChild(li);
    }
}
