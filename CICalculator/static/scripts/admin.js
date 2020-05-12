"use strict"; 

console.log("Admin toimii")

let testObject = {
    provider: "Pyryn Auto",
    price: 1000,
    months: 4,
    payers: 1,
}

function renderPayment(data) {
    processData(data);
}

function processData(obj) {
    $.each(obj, function(key, value) {
        console.log(key);
        console.log(value);
    });
}

function getResource(href, renderFunction) {
    $.ajax({
        url: href,
        success: renderFunction
    });
}

$(document).ready(function(){
    $("button").click(function(){
        getResource("/api/dummyhandle/plans", renderPayment); 
    }); 
});