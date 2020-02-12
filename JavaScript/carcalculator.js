//Car price calculator. On muokattu, ei ole enää niin alkuperäinen. Muokkauspäivä 23.1
function CarCalculate() {
  var carPrice = document.getElementById("car_price").value;
  var handmoney = document.getElementById("hand_money").value;//keksittävä käyttötarkoitus
  var partofmonth = document.getElementById("monthly_fee").value;//kuukausierä

  //validate input
  if (carPrice === "" || handmoney == 0) {
    alert("Please enter values");
    return;
  }
  //Check to see if this input is empty or less than or equal to 1
  if (partofmonth === "" || partofmonth <= 1) {
    partofmonth = 1;
    document.getElementById("Sold_of_car").style.display = "none";
  } else {
    document.getElementById("Sold_of_car").style.display = "block";
  }

  //Calculate car price
  var total = ((carPrice - handmoney)//tähän tulee sitten muut laskutoimitukset) / partofmonth;
  //round to two decimal places
  total = Math.round(total * 100) / 100;
  //next line allows us to always have two digits after decimal point
  total = total.toFixed(2);
  //Display the tip
  document.getElementById("totalprice").style.display = "block";
  document.getElementById("tipcar").innerHTML = total;//html rivi 36

}

//Hide the tip amount on load
document.getElementById("tipcar").style.display = "none";//html rivi 35
document.getElementById("Sold_of_car").style.display = "none";

//click to call function
document.getElementById("calculate").onclick = function() {
  CarCalculate();

};