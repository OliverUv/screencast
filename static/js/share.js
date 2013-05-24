$(document).ready(function(){
    //Slick clickable userlist
    $(".user").click(function(){
        var element = $(this);
        var added = false;
        var targetList = $(this).parent().siblings(".cleanlist")[0];
        $(this).fadeOut("fast", function() {
            $(".cleanlist", targetList).each(function(){
                if ($(this).text() > $(element).text()) {
                    $(element).insertBefore($(this)).fadeIn("fast");
                    added = true;
                    return false;
                }
            });
            if(!added) $(element).appendTo($(targetList)).fadeIn("fast");
        });
    });

    //Mark resources
    $(".resourceShareList").on("click", ".resourceMarked", function(event){
        //$(this).text().replace(/[>]/, "");
        $(this).text($(this).text().substr(2));
        $(this).removeClass().addClass("resourceUnmarked").fadeIn("fast");
    });

    $(".resourceShareList").on("click", ".resourceUnmarked", function(event){
        var clicked = $(event.target);
        var oldtext = $(clicked).text();
        $(clicked).text("> " +oldtext);
        $(clicked).removeClass().addClass("resourceMarked").fadeIn("fast");
    });
});
