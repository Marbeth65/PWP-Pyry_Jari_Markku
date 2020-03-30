//Car price calculator. On muokattu, ei ole enää niin alkuperäinen. Muokkauspäivä 17.2
function CarCalculate() {
  var carPrice = document.getElementById("car_price").value;
  var handmoney = document.getElementById("hand_money").value;//keksittävä käyttötarkoitus
  var percent = document.getElementById("interest_percent").value;//prosenttikorko
  var monthpay = document.getElementById("month_pay").value;//kuukausimaksu
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
  var reduced_price = ((carPrice - handmoney)//(1+(korkoprosentti%/100)) * autonhinta
  //round to two decimal places
  month_pay = Math.round(1+(percent / 100)) * reduced_price;
  //next line allows us to always have two digits after decimal point
  month_pay = month_pay.toFixed(2);
  //Display the tip
  document.getElementById("month_pay").style.display = "block";
  document.getElementById("interest_percent").innerHTML = total;//html rivi 36

}

//Hide the tip amount on load
document.getElementById("interest_percent").style.display = "none";//html rivi 35
document.getElementById("Sold_of_car").style.display = "none";

//click to call function
document.getElementById("calculate").onclick = function() {
  CarCalculate();

};