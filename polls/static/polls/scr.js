'use strict';

function detectDayBudget(budget, days=30){
    var dayBudget = budget / days;
    alert(dayBudget);
    return dayBudget;
}

function chooseOptExpenses(){
    for (var i=1; i<=3; i++){
        appData.optionalExpenses[i] = prompt("Статья необязательных расходов?");
    }
}
var money = +prompt("Ваш бюджет на месяц?", "");
var date = prompt("Введите дату в формате YYYY-MM-DD", "");

var appData = {
    budget: money,
    timeData: date,
    expenses: {},
    optionalExpenses: {},
    income: [],
    savings:  false
};
for (let i=0; i<2; i++){
    let expense = prompt("Введите обязательную статью расходов в этом месяце:", "питание");
    let bud = +prompt("Во сколько обойдется?", "12");
    appData.expenses[expense] = bud;
}

detectDayBudget(appData.budget);
chooseOptExpenses();
console.log(appData.optionalExpenses)


