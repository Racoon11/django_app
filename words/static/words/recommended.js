
function create(htmlStr) {
    var frag = document.createDocumentFragment(),
        temp = document.createElement('div');
    temp.innerHTML = htmlStr;
    while (temp.firstChild) {
        frag.appendChild(temp.firstChild);
    }
    return frag;
}
function createList(csrf) {
    document.getElementById("recom-list").remove();
    var code = '<div id="recom-list">';
    var words;
    var ids;
    var amount1 = document.getElementById("amount").value;
    var amount = fetch('/recommendation/five?amount=' + amount1)
      .then((response) => {return response.json();})
      .then((data) => {words = data['words']; ids = data['ids'];})
      .then((amount) => {
          for (var i=0; i < words.length; i++) {
            code += '<div class="row">' +
                    '<form action="/words/add" method="post">' +
                    '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf + '">' +
                    '<span class="word"><label>' + words[i] + '</label></span>' +
                    '<button type="submit" name="id" id="login-submit" style="margin: 2px"' +
                          'class="btn btn-primary"  value=' + ids[i] + '>+</button>' +
                    '</form>' + '</div>';
          }
          code += '</div>'
          return create(code);
      }).then ((fragment) => {
      var div = document.getElementById("scroll");
      div.appendChild(fragment);});
}

function createList2(words, ids, csrf) {
    words = words.split('&#x27;');
    var code = '';
    var words1 = [];
    for (var i=1; i < words.length; i+=2){
        words1.push(words[i]);
    }
    for (var i=0; i < words1.length; i++) {
        code += '<div class="row">' +
                '<form action="/words/add" method="post">' +
                '<input type="hidden" name="csrfmiddlewaretoken" value="' + csrf + '">' +
                '<span class="word"><label>' + words1[i] + '</label></span>' +
                '<button type="submit" name="id" id="login-submit" style="margin: 2px"' +
                      'class="btn btn-primary"  value=' + ids[i] + '>+</button>' +
                '</form>' + '</div>';
      }
    var fragment = create(code);
    var div = document.getElementById("div-search");
    div.appendChild(fragment);
}
