$(document).ready(function(){
    $("#submit").click(function(){
        $("#loading").fadeIn(); 
        $("#image").fadeOut();   
        $("#hide").fadeOut(); 
        $("#hide2").fadeOut();
        $("#submit").fadeOut(); 
    });

    $(window).on("load", function () {
        $("#loading").fadeOut(); 
        $("#image").fadeIn().css("display", "flex");  
        $("#hide").fadeIn().css("display", "flex");  
        $("#submit").fadeIn(); 
        $("#hide2").fadeIn(); 
    });
  });