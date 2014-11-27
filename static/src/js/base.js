var db=$(".van-db")
db.on("click", function(){
    $(this).next("li").slideToggle("fast");
});


$(".left-coll").on("click", function(){
    $(".left-coll").css({ "color":"#444"});
    $(this).css({"color":"#3d92c9"});
    return true;
});


