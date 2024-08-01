

class word {
    constructor(rus, eng, idx) {
        this.rus = rus;
        this.eng = eng;
        this.idx = idx;
        this.mistakes = [0, 0, 0, 0];
        this.progress = 0;
  }
}

var words = {};
var rusGlobal;
var engGlobal;
var idxGlobal;
var csrf;

function train(rusWords, engWords, idxs, csrftoken){


    rusWords = rusWords.split('&#x27;');
    var words1 = [];
    for (var i=1; i < rusWords.length; i+=2){
        words1.push(rusWords[i]);
    }
    engWords = engWords.split('&#x27;');
    var words2 = [];
    for (var i=1; i < engWords.length; i+=2){
        words2.push(engWords[i]);
    }
    rusGlobal = words1;
    engGlobal = words2;
    idxGlobal = idxs;
    for (var i=0; i < idxs.length; i++){
        words[idxs[i]] = new word(words1[i], words2[i], idxs[i]);
    }
    csrf = csrftoken;
    var idx = idxs[0];
    return first(idxs[0], words[idx].rus, words[idx].eng, rusGlobal, clickButton);

}

 function clickButton(choice){

        var j = idxGlobal.shift();
        document.getElementById("first").remove();

        if (choice.target.innerText != words[j].rus && words[j].mistakes[0] < 3){
            idxGlobal.push(j);
            words[j].mistakes[0] += 1;
        }
        if (idxGlobal.length == 0) {
            for (let key in words){
                idxGlobal.push(key);
            }
            var idx = idxGlobal[0];

            return first(idxGlobal[0], words[idx].eng, words[idx].rus, engGlobal, clickButton2);
        }
        var idx = idxGlobal[0];
        return first(idxGlobal[0], words[idx].rus, words[idx].eng, rusGlobal, clickButton);
    }

function clickButton2(choice){
    var j = idxGlobal.shift();
    document.getElementById("first").remove();
    if (choice.target.innerText != words[j].eng && words[j].mistakes[1] < 3){
        idxGlobal.push(j);
        words[j].mistakes[1] += 1;
    }
    if (idxGlobal.length == 0) {
            for (let key in words){
                idxGlobal.push(key);
            }
            var idx = idxGlobal[0];

            return third(idxGlobal[0], words[idx].eng, words[idx].rus);
        }
    var idx = idxGlobal[0];
    return first(idxGlobal[0], words[idx].eng, words[idx].rus, engGlobal, clickButton2);
}

    function first(idx, rus, eng, optionsGlobal, clickFunc){

        var mainDiv = document.createElement('div');
        mainDiv.className = "container h-100";
        mainDiv.id = "first";

        var div = document.createElement('div');
        div.className = "col-md-12 col-md-offset-3";

        var engH3 = document.createElement('h3');
        engH3.className = "mx-4 text-center";
        engH3.textContent = eng;
        div.appendChild(engH3);
        mainDiv.appendChild(div);

        var divButtons = document.createElement('div');
        divButtons.className = "col-md-12 h-100";
        divButtons.align = "center";
        options = [rus];
        var i = 0;
        while(options.length < 4){
            var elem = optionsGlobal[i];
            if (elem == rus) {
                i++;
                continue;
            }
            options.push(elem);
            i++;
        }
        options.sort(randomSort);
        for (var i=0; i<4; i++) {
            var but = document.createElement('button');
            but.className = "btn btn-primary btn-lg m-3 col-md-4";
            but.textContent = options[i];
            but.onclick = clickFunc.bind(this);
            divButtons.appendChild(but);
        }
        mainDiv.appendChild(divButtons);
        document.body.appendChild(mainDiv);
    }

function third(idx, eng, rus){
    var mainDiv = document.createElement('div');
    mainDiv.className = "container h-100";
    mainDiv.id = "third";

    var div = document.createElement('div');
    div.className = "col-md-12 col-md-offset-3";

    var engH3 = document.createElement('h3');
    engH3.className = "mx-4 text-center";
    engH3.textContent = rus;

    var ans = document.createElement('div');
    ans.className = "mx-4 text-center";
    ans.id = "answer";

    for (var i=0; i < eng.length; i++){
        var letter = document.createElement('button');
        letter.className = "btn btn-light btn-lg border border-primary";
        letter.id = "btn" + i;
        letter.textContent = ".";
        letter.disabled = true;
        ans.appendChild(letter);
    }

    div.appendChild(engH3);
    div.appendChild(ans);
    mainDiv.appendChild(div);

    var divButtons = document.createElement('div');
    divButtons.className = "col-md-12 h-100";
    divButtons.align = "center";
    var engSorted = eng.split('');
    engSorted.sort(randomSort);
    for (var i=0; i < eng.length; i++){
        var but = document.createElement('button');
        but.className = "btn btn-primary btn-lg m-3";
        but.textContent = engSorted[i];
        but.onclick = clickButton3.bind(this);
        divButtons.appendChild(but);
    }


    mainDiv.appendChild(divButtons);
    document.body.appendChild(mainDiv);

}
function clickButton3(but){
    var idx = idxGlobal[0];
    var clickedChar = but.target.innerText;
    var word = words[idx];
    var realChar = word.eng[word.progress];
    if (clickedChar == realChar){
        var label = document.getElementById("btn" + word.progress);
        label.textContent = word.eng.slice(word.progress, ++word.progress);
        but.srcElement.remove(); // ??
        if (word.progress >= word.eng.length){
            document.getElementById("third").remove();
            word.progress = 0;
            idxGlobal.shift();
            if (idxGlobal.length == 0) {
                for (let key in words){
                    idxGlobal.push(key);
                }
                idx = idxGlobal[0];

                return fourth(idxGlobal[0], words[idx].eng, words[idx].rus);
            }
            idx = idxGlobal[0];
            return third(idx, words[idx].eng, words[idx].rus);
        }
    }
    else {
        word.mistakes[2]++;
    }
}
function randomSort(c, d){
    var a = -1000;
    var b = 1000;
    return Math.random()*(b-a)+a;
}
function fourth(idx, eng, rus){
    var mainDiv = document.createElement('div');
    mainDiv.className = "container h-100";
    mainDiv.id = "fourth";

    var div = document.createElement('div');
    div.className = "col-md-12 col-md-offset-3";
    div.align = "center";

    var engH3 = document.createElement('h3');
    engH3.className = "mx-4 text-center";
    engH3.textContent = rus;


    var inpDiv = document.createElement("div");
    inpDiv.className = "col-md-4 h-100";

	var inp = document.createElement("input");
	inp.type = 'text';
	inp.className = "form-control";
	inp.id = "inputWord";
	inp.autofocus="autofocus";
	inp.focus();
	var but = document.createElement("button");
	but.className = "btn btn-primary btn-lg m-3";
    but.textContent = "submit";
    but.onclick = clickButton4.bind(this);

	inpDiv.appendChild(inp);
	inpDiv.appendChild(but);
	div.appendChild(engH3);
    div.appendChild(inpDiv);
    mainDiv.appendChild(div);
    document.body.appendChild(mainDiv);
}

function clickButton4(button){
    var inp = document.getElementById("inputWord").value;
    var idx = idxGlobal[0];
    var word = words[idx];
    document.getElementById("fourth").remove();
    if (inp != word.eng) {
        word.mistakes[3]++;
    }

    var mainDiv = document.createElement('div');
    mainDiv.className = "container h-100";
    mainDiv.id = "fourth";

    var div = document.createElement('div');
    div.className = "col-md-12 col-md-offset-3";
    div.align = "center";

    var engH3 = document.createElement('h3');
    engH3.className = "mx-4 text-center";
    engH3.textContent = word.eng;

    var ans = document.createElement('h3');
    ans.className = "mx-4 text-center";
    ans.id = "answer";
    ans.textContent = inp;

    if (inp != word.eng) {
        ans.style.color = "red";
    }
    else {
        ans.style.color = "green";
    }

    var but = document.createElement("button");
	but.className = "btn btn-primary btn-lg m-3";
    but.textContent = "next";
    but.autofocus="autofocus";
    if (inp != word.eng) {
        but.id = "false";
        but.onclick = clickButton5.bind(but);
    } else{
        but.id = "true";
        but.onclick = clickButton5.bind(but);
    }


    div.appendChild(engH3);
    div.appendChild(ans);
    div.appendChild(but);
    mainDiv.appendChild(div);
    document.body.appendChild(mainDiv);
}

function clickButton5(event){
    document.getElementById("fourth").remove();
    var j = idxGlobal.shift();
    var correct = event.srcElement.id;

    if (correct=="false" && (words[j].mistakes[3] < 3)) {
        idxGlobal.push(j);
    }
    if (idxGlobal.length == 0) {
            return loadFinal();

        }
        else {
            var idx = idxGlobal[0];
            return fourth(idx, words[idx].eng, words[idx].rus);

        }

}

function loadFinal(){
    var info = {};
    for (let key in words) {
        info[key] = words[key].mistakes.reduce((partialSum, a) => partialSum + a, 0);
    }
    fetch("/words/train/finish", {
      method: "POST",
      body: JSON.stringify(info),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
        "X-CSRFToken": csrf
      }
    });

    var mainDiv = document.createElement('div');
    mainDiv.className = "container h-100";
    mainDiv.align = "center";

    var div = document.createElement('div');
    div.className = "col-md-12 col-md-offset-3";
    div.align = "center";
    console.log(words);
    for (var i in words){
        var div2 = document.createElement('div');
        div2.className = "row";
        var ans = document.createElement('h3');
        ans.className = "col-md-8";
        ans.textContent = words[i].eng + ' - ' + words[i].rus;

        var cor = document.createElement('h3');
        cor.className = "col-md-2";
        cor.textContent = info[i];
        if (info[i] == 0) {
            cor.style.color = "green";
        } else {
            cor.style.color = "red";
        }
        div2.appendChild(ans);
        div2.appendChild(cor);
        div.appendChild(div2);
    }
    var but = document.createElement('button');
    but.className = "btn btn-primary btn-lg m-3";
    but.textContent = "back";
    but.autofocus="autofocus";
    but.onclick = function () {
        location.href = "/words/mywords";
    };
    div.appendChild(but);
    mainDiv.appendChild(div);
    document.body.appendChild(mainDiv);
}
