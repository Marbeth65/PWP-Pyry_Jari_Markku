//Car price calculator. On muokattu, ei ole enää niin alkuperäinen. Muokkauspäivä 23.1
function CarCalculate() {
  var carPrice = document.getElementById("feed car price").value;
  var serviceQual = document.getElementById("somethingsomething").value;//keksittävä käyttötarkoitus
  var partofmonth = document.getElementById("part of month").value;//kuukausierä

  //validate input
  if (carPrice === "" || serviceQual == 0) {
    alert("Please enter values");
    return;
  }
  //Check to see if this input is empty or less than or equal to 1
  if (partofmonth === "" || partofmonth <= 1) {
    partofmonth = 1;
    document.getElementById("each").style.display = "none";
  } else {
    document.getElementById("each").style.display = "block";
  }

  //Calculate tip
  var total = (carPrice * serviceQual) / partofmonth;
  //round to two decimal places
  total = Math.round(total * 100) / 100;
  //next line allows us to always have two digits after decimal point
  total = total.toFixed(2);
  //Display the tip
  document.getElementById("totalprice").style.display = "block";
  document.getElementById("tip").innerHTML = total;

}

//Hide the tip amount on load
document.getElementById("totalprice").style.display = "none";
document.getElementById("each").style.display = "none";

//click to call function
document.getElementById("calculate").onclick = function() {
  CarCalculate();

};