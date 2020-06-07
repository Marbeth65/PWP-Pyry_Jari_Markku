"use strict"; 

console.log("Models toimii");

let modelIndex = 0;                 // This variable stores the index from which models are added to fields
let model1_link = "";               // these are hypermedialinks that are taken after GET request to item
let model2_link = "";
let model3_link = "";
let modelContainer_link = {};

function postModel(){
    // While posting models all fields are mandatory
    
    let $manufacturer = $("#manufacturerInput");
    let $model = $("#modelInput");
    let $year = $("#yearInput");
    
    let postObject = {
    model: $model.val(),
    year: parseInt($year.val()),
    manufacturer: $manufacturer.val(),
    }

    $.ajax({
        type: "POST",
        url: "/api/dummyhandle/models",
        data: JSON.stringify(postObject),
        contentType: "application/json",
        success: printSuccess,
        error: printError
    });
}
function printSuccess(){
    alert("success");
}
function printError() {
    alert("error!");
}

function getResource(href, renderFunction) {
    $.ajax({
        url: href,
        success: renderFunction
    });
}

function appendModelTable(object){
    
    // this function simply appends data to tables. It is fed in packs of up to 3
    // input object is the response returned from GET call to Model Collection that has been divided by renderModels function
    
    let $modelCont1 = $("#models1 > table"); 
    let $modelCont2 = $("#models2 > table");
    let $modelCont3 = $("#models3 > table");
    
    $modelCont1.empty()
    $modelCont2.empty()
    $modelCont3.empty()
    
    $.each(object[0], function(key, value){
        if ((key == "@controls") || (key == "@namespaces")) {
            
        } else {
        let row = "<tr><td>" + key + "</td><td>" + value + "</td></tr>"
        $modelCont1.append(row);
        }
    });
    
    model1_link = object[0]["@controls"]["self"]["href"];
    
    if (object.length > 1) {
    
    $.each(object[1], function(key, value){
        if ((key == "@controls") || (key == "@namespaces")) {
            
        } else {
        let row = "<tr><td>" + key + "</td><td>" + value + "</td></tr>"
        $modelCont2.append(row);
        }
    });  
    model2_link = object[1]["@controls"]["self"]["href"];
    }
    
    if (object.length > 2) {
    
    $.each(object[2], function(key, value){
        if ((key == "@controls") || (key == "@namespaces")) {
            
        } else {
        let row = "<tr><td>" + key + "</td><td>" + value + "</td></tr>"
        $modelCont3.append(row);
        }
    });
    model3_link = object[2]["@controls"]["self"]["href"]; 
    }
};
function renderModels(data){
    let i;
    let pack = [];
    let plan;
    
    // this function feeds paymentplans to appendModelTable
    // data input is part of the response from Model Collection that has been divided into smaller packages
    
    for (i = 0; i < modelIndex; i++) { // Datan esikäsittely
        data["items"].shift();
    }
    for (i = 0; i < 3; i++) {
        let len = (Object.keys(data["items"])).length;

        if (len > 0) {
        plan = data["items"].shift();
        pack.push(plan);
        } else {
            
        }
    }
    appendModelTable(pack);
    modelIndex += 3;
}

function renderModelItem1(data) {
    // This function projects individual plan to Model item box.
    // Parameter data is response from GET request to Model Item
    
    
    let $modelItemTable = $("#modelItem > table");
    $modelItemTable.empty();
    
    $modelItemTable.append("<tr><td>Manufacturer:</td><td>" + data["manufacturer"] + "</td></tr>");
    $modelItemTable.append("<tr><td>Model:</td><td>" + data["model"] + "</td></tr>");
    $modelItemTable.append("<tr><td>year:</td><td>" + data["year"] + "</td></tr>");
    
    modelContainer_link = data;     // this data isnt use as it is since I can use hypermedia instead.
}

$(document).ready(function(){
    getResource("/api/dummyhandle/models", renderModels);
    
    $("#modelForthButton").click(function(){
    getResource("/api/dummyhandle/models", renderModels);    
    });
    
    $("#postm").click(function(){
    postModel();
    });
    
    $("#models1").click(function(){
        // these if statements make sure that you cant browse models when there is already associated model
        
        if (assoModel == false){
        getResource(model1_link, renderModelItem1);
        }
    });
    
    $("#models2").click(function(){
        if (assoModel == false){
        getResource(model2_link, renderModelItem1);
        }
    });
    
    $("#models3").click(function(){
        if (assoModel == false){
        getResource(model3_link, renderModelItem1);
        }
    });
});