$(document).ready(function(){
    $("#upload").click(function(){
        $("#loading-excel").fadeIn(); 
        $("#loading-address").fadeIn(); 
        $("#content").fadeOut();   
    });

    $(window).on("load", function () {
        $("#loading-excel").fadeOut(); 
        $("#loading-address").fadeOut(); 
        $("#content").fadeIn();  
    });
  });