"use strict"; 

console.log("Admin toimii");
let imgData;
let responseData;
let currentAlbumHash;

let albumInfo = {
    "url": "https://api.imgur.com/3/album/HGmZG13",
    "core": "https://api.imgur.com/3/album/"
}
let clientInfo = {
    clientID: "f4feaec8a58cda2"
}

let simpleHeader = {
    Authorization: "Client-ID " + clientInfo["clientID"],
    Accept: 'application/json'
}

let newAlbumInfo = {
    "data": {
        "id": "7hFM6ug",
        "deletehash": "m2mgsHwJlUYbVk4"
    },
    "success": true,
    "status": 200
}

let kuvaKansioRoute = "C:/Users/user/Desktop/ProgrammableWeb/Koodia_ja_Tehtavia/requests";

let ajaxHeaderInfo = {
    type: "GET",
    url: albumInfo["core"] + newAlbumInfo["data"]["id"],
    headers: simpleHeader,
    success: function(data){
        console.log(data["data"]);
        $.each(data["data"]["images"], function(index, item){
            let $contents = $(".contents");
            
            console.log(item["link"]);
            let row = "<img src=\"" + item["link"] + "\">";
            console.log(row);
            $contents.append(row);
        });
    }
    
}

function postImage(url){
    
    // This function allows you to post image to current album. Copy-paste url to input field and press submit button.
    // Parameter url: the url of the image you want to add to album
    
    
    currentAlbumHash = localStorage.album;
    if (currentAlbumHash == undefined) {
        console.log("Create album first!");
    } else {
    currentAlbumHash = JSON.parse(currentAlbumHash);
    currentAlbumHash = currentAlbumHash.data.deletehash;
    
    let ajaxPostCall = {
        url: "https://api.imgur.com/3/image", 
        type: "POST",
        headers: simpleHeader,
        data: {
            image: url,
            type: "url",
            album: currentAlbumHash
        },
        success: function(data){
            console.log("Success!");
            appendImgDataToLocal(data["data"]);
        },
        error: function(data){
            console.log(data);
        }
    }
    
    $.ajax(ajaxPostCall);
    }
}

function appendImgDataToLocal(imageInfo){
    
    // This is used if you want to store information about pictures to your local storage.
    // Parameter imageInfo is an object that comes as a response from succesful posting
    
    let imageIds = localStorage.images;
    if (imageIds == undefined) {
    localStorage.setItem("images", JSON.stringify([]));
    }
    imageIds = JSON.parse(imageIds);
    imageIds.push(imageInfo);
    localStorage.setItem("images", JSON.stringify(imageIds));
};

function delByKey(key){
    
    // Deletes key from local storage
    // Key is key from object that you want to delete.
    
    localStorage.removeItem(key);
}

function viewImages(){
    
    // for viewing image data on console.
    
    let images = JSON.parse(localStorage.getItem("images"));
    
    $.each(images, function(index, item){
        console.log(index, item);
    });
}

function delImages(hash){
    // Deletes images from gallery and storage
    // hash is albums deletehash that is given when album is created.
    
    
    let storageHash = localStorage.album;
    if (storageHash == undefined) {
        console.log("No album to delete");
    } else {

    storageHash = JSON.parse(storageHash);
    let albumHash = storageHash.data.deletehash;
    
    let ajaxCallDelImages = {
        type: "POST",
        url: "https://api.imgur.com/3/album/" + albumHash + "/remove_images",
        headers: simpleHeader,
        success: function(data){
            console.log("success");
        },
        error: function(){
            console.log("error");
        },
        data: {
            ids: hash,
        }
    };
    $.ajax(ajaxCallDelImages);
    delByKey("images");
    }
}

function getHashes(){
    
    // Gets imagehashes that are used in many modifying operations
    // Returns array of images deletehashes that can be used to operate on the images
    
    
    let images = JSON.parse(localStorage.getItem("images"));
    let imgArray = []
    
    $.each(images, function(index, item){
        console.log(item.deletehash);
        imgArray.push(item.deletehash);
    });
    return imgArray;
}

function generateAlbum(){
    // This needs to be run once before you can post images to album. This generates album
    
    let albumPostCall = {
        type: "POST",
        headers: simpleHeader,
        url: "https://api.imgur.com/3/album",
        data: {
            title: "Car Collection",
            deletehashes: getHashes(),
        },
        success: function(data){
            console.log("success");
            localStorage.setItem("album", JSON.stringify(data));    // Data gets stored to localStorage
        },
        error: function(data){
            console.log(data);
        }
        
    }
    $.ajax(albumPostCall);
}

function viewAlbum(){
    
    // Sends get request to Imgur API:s Get album resource and appends images to webpage.
    
    
    let albumHash = JSON.parse(localStorage.getItem("album"));
    albumHash = albumHash.data.id;
    
    console.log(albumHash);
    
    let viewAlbumCall = {
        type: "GET",
        url: "https://api.imgur.com/3/album/" + albumHash,
        headers: simpleHeader,
        success: function(data){
            console.log(data);
            $.each(data["data"]["images"], function(index, data){
                let $contents = $(".contents");
                let item = "<img src=\"" + data["link"] + "\">";
                console.log(item);
                
                $contents.append(item);
            });
        },
        error: function(data){
            console.log(data.errorText);
        }
    }
    $.ajax(viewAlbumCall);
}

$(document).ready(function(){
    

    
    $("#submitImageButton").click(function(){
        let input = $("#urlfield");
        
        postImage(input.val());
    });
    
    $("#viewImageButton").click(function(){
        
        viewImages();
        viewAlbum();
    });
    
    $("#deleteButton").click(function(){
        console.log(localStorage.images);
    });
    
});