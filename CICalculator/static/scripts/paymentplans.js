"use strict"; 

console.log("Admin toimii")

let AllIndex = 0;
let AllPaymentIndex = 0;
let All1_link = "";
let All2_link = "";
let All3_link = "";
let assoModel = false;
let paymentContainer_link = {};

// This function feeds data to the fucntion that handles paymentplan browsing

function renderPayment(data) {
    let i;
    let pack = [];
    
    // shift data until desired index is met
    
    for (i = 0; i < AllIndex; i++) {
        data["items"].shift();
        console.log("Shifted");
    }
    
    for (i = 0; i < 3; i++) {
        let keys = Object.keys(data["items"]);
        if (keys.length > 0) {
        let plan = data["items"].shift();
        pack.push(plan);
        } else {
            console.log("loppu");
        }
    }
    appendTable(pack);
    AllIndex = AllIndex + 3;
    }

function postPayment(){
    // For posting paymentplans
    
    let $provider = $("#providerButton");
    let $price = $("#priceButton");
    let $months = $("#monthButton");
    let $payers = $("#payersButton");
    let $interestrate = $("#interestrateButton");
    
    let postObject = {
        provider: $provider.val(),
        price: parseFloat($price.val()),
        months: parseInt($months.val()),
        payers: parseInt($payers.val()),
    }    
    
    if ($interestrate.val() != ""){
        postObject["interestrate"] = parseFloat($interestrate.val()); // interestrate is optional
    } else {
        postObject["interestrate"] = 0;
    }
    
    $.ajax({
    type: "POST",
    url: "/api/dummyhandle/plans",
    data: JSON.stringify(postObject),
    contentType: "application/json",
    success: function(){
        $("#postMessages").empty();
        $("#postMessages").append("Product added");
    },
    error: function(){
        $("#postMessages").empty();
        $("#postMessages").append("Error");
    }
    });
}    

function appendTable(object){
    
    // data from render payment is fed here to be appended to html tables
    
    let $AllCont1 = $("#All1 > table"); 
    let $AllCont2 = $("#All2 > table");
    let $AllCont3 = $("#All3 > table");
    
    $AllCont1.empty()
    $AllCont2.empty()
    $AllCont3.empty()
    
    $.each(object[0], function(key, value){
        if ((key == "@controls") || (key == "@namespaces")) {

        } else {
        let row = "<tr><td>" + key + "</td><td>" + value + "</td></tr>"
        $AllCont1.append(row);
        }
    });
    
    All1_link = object[0]["@controls"]["self"]["href"];         // hypermedialink to mempory
    console.log(All1_link)
    if (object.length > 1) {
    
    $.each(object[1], function(key, value){
        if ((key == "@controls") || (key == "@namespaces")) {
            
        } else {
        let row = "<tr><td>" + key + "</td><td>" + value + "</td></tr>"     // apend table. It appears to be missing ; but I dont want to touch it since it works
        $AllCont2.append(row);
        }
    });  
    All2_link = object[1]["@controls"]["self"]["href"];         // and here
    console.log(All2_link);
    }
    
    if (object.length > 2) {
    
    $.each(object[2], function(key, value){
        if ((key == "@controls") || (key == "@namespaces")) {
            
        } else {
        let row = "<tr><td>" + key + "</td><td>" + value + "</td></tr>"
        $AllCont3.append(row);
        }
    });
    All3_link = object[2]["@controls"]["self"]["href"];         // and here
    console.log(All3_link);
    }
};

function getResource(href, renderFunction) {
    // This has been taken from lovelace and modified slightly.
    // I left out the error part.
    
    $.ajax({
        url: href,
        success: renderFunction
    });
}

function renderItem(data) {
    let $payment = $("#paymentPlanItem > table");
    let $model = $("#modelItem > table");
    let $paymentInfo = $("#paymentPlanInfo");
    let iPrice;
    
    // clear previous data
    
    $payment.empty();
    $model.empty();
    $paymentInfo.empty();
    
    // Append information
    
    $payment.append("<tr><td>Provider:</td><td>" + data.provider + "</td></tr>");
    $payment.append("<tr><td>Price:</td><td>" + data.price + "</td></tr>");
    $payment.append("<tr><td>Interestrate:</td><td>" + data.interestrate + "</td></tr>");
    $payment.append("<tr><td>Months:</td><td>" + data.months + "</td></tr>");
    $payment.append("<tr><td>Payers:</td><td>" + data.payers + "</td></tr>");
    
    if (data.model != "No model") {         // if there is model it is appended
    $model.append("<tr><td>Model:</td><td>" + data.model + "</td></tr>");
    $model.append("<tr><td>manufacturer:</td><td>" + data.manufacturer + "</td></tr>");
    $model.append("<tr><td>year:</td><td>" + data.year + "</td></tr>");
    assoModel = true;
    modelContainer_link = {}
    } else {
        $model.append("<tr><td>No model</td></tr>"); // signs that there is no model
        assoModel = false;                              // this boolean prevents browsing models when there is already model associated
        modelContainer_link = {}
    }
    
    if (data.open == true) {
        $("#openButton").empty();
        $("#openButton").append("Close");
    } else {
        $("#openButton").empty();
        $("#openButton").append("Open");        
    }
    
    iPrice = Math.round(data.price * (1 + (data.interestrate / 100)));
    $paymentInfo.append("<p>Kokonaishinta on " + iPrice + " ja yksittäisen henkilön kuukausihinta on: " + ((iPrice / data.months) / data.payers) + "</p>"); // some basic information
    
    paymentContainer_link = data;       // taking dictionary to memory since it can be used to send POST requests
}
$(document).ready(function(){
    
    getResource("/api/dummyhandle/plans", renderPayment);
    
    $("#Allforthbutton").click(function(){
        getResource("/api/dummyhandle/plans", renderPayment);
    });
    
    $("#All1").click(function(){
        getResource(All1_link, renderItem);
    });
    
    $("#All2").click(function(){
        getResource(All2_link, renderItem);
    });
    
    $("#All3").click(function(){
        getResource(All3_link, renderItem);
    });
    
    $("#postp").click(function(){
        postPayment();
    });
});