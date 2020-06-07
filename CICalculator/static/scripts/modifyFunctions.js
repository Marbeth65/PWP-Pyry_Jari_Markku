"use strict"; 

console.log("modifyFunctions toimii");

function connectModel(){
    if ((modelContainer_link["manufacturer"] != undefined) || (paymentContainer_link["provider"] != undefined)){
    
    let Url = "/api/dummyhandle/models/"
    + modelContainer_link["manufacturer"] + "/"
    + modelContainer_link["model"] + "/"
    + modelContainer_link["year"];
    
    let paymentplanObj = {
        paymentplan_provider: paymentContainer_link["provider"],
        paymentplan_price: paymentContainer_link["price"],
        paymentplan_months: paymentContainer_link["months"]
    }
    
    let ajaxCallObj = {
        type: "POST",
        url: Url,
        data: JSON.stringify(paymentplanObj),
        contentType: "application/json",
        success: function(){
                let $paymentInfo = $("#paymentPlanInfo");
                
                $paymentInfo.empty();
                $paymentInfo.append("<p>Connected</p>");
        },
        error: renderError
    }
    $.ajax(ajaxCallObj);
    } else {
        console.log("Ei modelia tai plania");
    }
}

function delPayment() {
    if (paymentContainer_link["provider"] != undefined) {
        let payment_url = "/api/dummyhandle/plans/"
        + paymentContainer_link["provider"] + "/"
        + paymentContainer_link["price"] + "/"
        + paymentContainer_link["months"];
        
        console.log(payment_url);
        let ajaxCallObj = {
            type: "DELETE",
            url: payment_url,
            success: function(){
                let $paymentInfo = $("#paymentPlanInfo");
                
                $paymentInfo.empty();
                $paymentInfo.append("<p>Deleted</p>");
            },
            error: function(){
                let $paymentInfo = $("#paymentPlanInfo");
                
                $paymentInfo.empty();
                $paymentInfo.append("<p>Error</p>");                
            }
        }
        $.ajax(ajaxCallObj);
    } else {
        console.log("No payment");
    }
}

function renderError(errorData){
    let msg = errorData.responseJSON["@error"];
    console.log(msg);
}

function toggleOpen(){
    if (paymentContainer_link["provider"] != undefined) {
        let payment_url = "/api/dummyhandle/plans/"
        + paymentContainer_link["provider"] + "/"
        + paymentContainer_link["price"] + "/"
        + paymentContainer_link["months"];

        console.log(payment_url);
        
        let ajaxCallObj = {
            type: "PUT",
            url: payment_url,
            success: function(){
                let $paymentInfo = $("#paymentPlanInfo");
                
                $paymentInfo.empty();
                $paymentInfo.append("<p>Toggled</p>");                
            },
            error: function(){
                let $paymentInfo = $("#paymentPlanInfo");
                
                $paymentInfo.empty();
                $paymentInfo.append("<p>Error</p>");                 
            }
        }
        $.ajax(ajaxCallObj);
    } else {
        console.log("no plan");
    }
}

$(document).ready(function(){
    
    $("#addButton").click(function(){
        connectModel();
    });
    
    $("#delButton").click(function(){
        delPayment();
    });
    
    $("#openButton").click(function(){
        toggleOpen();
    });    
});