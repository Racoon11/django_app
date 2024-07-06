

function createButton2(words, idxs, csrf_token){

    var idxs = idxs.split(', ');
    idxs[0] = idxs[0].slice(1, idxs[0].length);
    idxs[idxs.length-1] = idxs.at(-1).slice(0, idxs.at(-1).length-1)
    for (var i=0; i < idxs.length; i++){
        idxs[i] = parseInt(idxs[i]);
    }
    var words = words.split('&#x27;');
    var words2 = [];
    for (var i=1; i < words.length; i+=2){
        words2.push(words[i]);
    }

    var div = document.createElement('div');
    div.className = "container h-100";

    var div2 = document.createElement('div');
    div2.className = "row h-100 justify-content-center align-items-center";

    var div3 = document.createElement('div');
    div3.className = "col-md-12 col-md-offset-3";

    var div4 = document.createElement('div');
    div4.className = "row";

    var title = document.createElement('h3');
    title.textContent = "My dictionary (words at all: " + idxs.length.toString() + ")";

    div4.appendChild(title);

    for (var i=0; i < idxs.length; i++){
        var divRow = document.createElement("div");
        divRow.className = "col-md-4"
        var wordTitle = document.createElement("h7");
        wordTitle.textContent = words2[i];
        divRow.appendChild(wordTitle);

        var nobr = document.createElement("nobr");
		var subForm = document.createElement("form");
		subForm.action = "/words/mywords";
		subForm.method = "post";
		subForm.className = "nospace";

		var inp = document.createElement("input");
		inp.type = "hidden";
		inp.name = "csrfmiddlewaretoken";
		inp.value = csrf_token;
		inp.className = "nospace";
		subForm.appendChild(inp);

		/*var nobr = document.createElement("nobr");
        divRow.appendChild(nobr);*/

		var butt = document.createElement("button");
		butt.type = "submit";
		butt.name = "id";
		butt.className = "btn btn-sm btn-primary nospace";
		butt.value = idxs[i];
		butt.textContent = "del";
		subForm.appendChild(butt);

		nobr.appendChild(subForm);
        divRow.appendChild(nobr)
        div4.appendChild(divRow);
    }


    div3.appendChild(div4);
    div2.appendChild(div3);
    div.appendChild(div2);
    document.body.appendChild(div);
}
