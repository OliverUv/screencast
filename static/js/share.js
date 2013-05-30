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

    $(".sharebutton").on("click", function(){
        //Get all marked resources
        var rs = [], lis = document.getElementById("resourcelist").getElementsByClassName("resourceMarked");
        for(var i=0, im=lis.length; im>i; i++)
            rs.push(lis[i].firstChild.nodeValue.substr(2));

        //Get all selected users
        var usr = [], lis = document.getElementById("sharelist").getElementsByClassName("user");
        for(var i=0, im=lis.length; im>i; i++)
            usr.push(lis[i].firstChild.nodeValue);
        
        var resources = JSON.stringify(rs);
        var users = JSON.stringify(usr);
        
        $.ajax({
            url: "share/", 
            type: "POST",
            dataType: "html",
            data: {
                'resources': resources,
                'sharedusers': users,
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

    // CSRF --------------------------------------
    jQuery(document).ajaxSend(function(event, xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        function sameOrigin(url) {
            // url could be relative or scheme relative or absolute
            var host = document.location.host; // host + port
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;
            // Allow absolute or scheme relative URLs to same origin
            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }
        function safeMethod(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    });
});
