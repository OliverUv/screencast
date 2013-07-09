$(document).ready(function(){
    //Switch position from one list to the other sibling list
    function switchList(){
        var element = $(this);
        var added = false;
        var targetList = $(this).parent().siblings(".cleanlist")[0];
        $(this).fadeOut("fast", function() {
            $(".user, .group", targetList).each(function(){
                if ($(this).text().toLowerCase() > $(element).text().toLowerCase()) {
                    $(element).insertBefore($(this)).fadeIn("fast");
                    added = true;
                    return false;
                }
            });

            if(!added) $(element).appendTo($(targetList)).fadeIn("fast");
        });
    }
    
    $(".user").click(switchList);
    $(".group").click(switchList);

    //Mark resources
    $(".resourceShareList").on("click", ".resourceMarked", function(event){
        $(this).text($(this).text().substr(2));
        $(this).removeClass().addClass("resourceUnmarked").fadeIn("fast");
    });

    $(".resourceShareList").on("click", ".resourceUnmarked", function(event){
        var clicked = $(event.target);
        var oldtext = $(clicked).text();
        $(clicked).text("> " +oldtext);
        $(clicked).removeClass().addClass("resourceMarked").fadeIn("fast");
    });

    $("#sharebutton").on("click", function(){
        //Get all marked resources
        var rs = [], lis = document.getElementById("resourcelist").getElementsByClassName("resourceMarked");
        for(var i=0, im=lis.length; im>i; i++)
            rs.push(lis[i].firstChild.nodeValue.substr(2));

        //Get all selected users
        var usr = [], lis = document.getElementById("sharelist").getElementsByClassName("user");
        for(var i=0, im=lis.length; im>i; i++)
            usr.push(lis[i].firstChild.nodeValue);
        
        //Get all selected groups
        var gr = [], lis = document.getElementById("sharelist").getElementsByClassName("group");
        for(var i=0, im=lis.length; im>i; i++)
            gr.push(lis[i].firstChild.nodeValue);

        var resources = JSON.stringify(rs);
        var users = JSON.stringify(usr);
        var groups = JSON.stringify(gr);
        
        $.ajax({
            url: "share/", 
            type: "POST",
            dataType: "html",
            data: {
                'resources': resources,
                'users': users,
                'groups': groups,
                },
                success: function(html){
                    $('#result').html(html);
                },
                error: function(xhr,errmsg,err){
                    alert(xhr.status + ": " + xhr.responseText);
                }
        });
        return false;
    });
});
