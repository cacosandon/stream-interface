$(document).ready(function(){
    $("#submit").click(function(){
        $("#loading").fadeIn(); 
        $("#image").fadeOut();   
        $("#hide").fadeOut(); 
        $("#submit").fadeOut(); 
    });

    $(window).on("load", function () {
        $("#loading").fadeOut(); 
        $("#image").fadeIn().css("display", "flex");  
        $("#hide").fadeIn().css("display", "flex");  
        $("#submit").fadeIn(); 
    });
  });