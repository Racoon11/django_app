

function changeInfo(firstname, lastname, level){
    var fnInput = document.getElementById("firstName");
    fnInput.placeholder = firstname;
    var lnInput = document.getElementById("lastName");
    lnInput.placeholder = lastname;
    var levelInput = document.getElementById("level");
    for(var i, j = 0; i = levelInput.options[j]; j++) {
        if(i.value == level) {
            levelInput.selectedIndex = j;
            break;
        }
    }
}
