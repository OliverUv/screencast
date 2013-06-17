$(document).ready(function(){
    $.fn.exists = function () {
        return this.length !== 0;
    }

    $.fn.addRemoveViewButton = function (){
        var viewButton = $(this.find(".viewbutton"));
        if (viewButton.exists()){
            viewButton.remove().fadeIn("fast");
        }
        else{
            this.prepend("<div class='viewbutton'>[+]</div>").fadeIn("fast");
        }
    }

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

            //View group button remove/add
            if (element.hasClass("group")){
                element.addRemoveViewButton();
            }
        });
    }
    
    $(".user").not('.viewbutton').click(switchList);
    $(".group").not('.viewbutton').click(switchList);

    //View a group
    $(".viewbutton").on("click", function(){
        var selectedgroup = JSON.stringify($(this).parent().text().substr(3));
        //Get group users and add them to an ul
        $.ajax({
            url: "get_group/",
            type: "POST",
            dataType: "json",
            data:{
                'group': selectedgroup, 
            },
            success: function(data){
                //Add headline for list
                $('#groupview p').text('Users in ' + selectedgroup +':');
                //Clear list
                var target = $('#groupview ul');
                target.empty();
                //Add users to div
                var usrlist = data.users.split(' ');
                $(usrlist).each(function() {
                    $('<li>'+this+'</li>').appendTo(target);
                });
                
                $('#result').html(data.users + ' Message:' + data.message);
            },
            error: function(xhr){ alert('Error: ' + xhr.status);}
        });
    });
    
    //Create a group 
    $("#groupbutton").on("click", function(){
        //Get all selected users
        var usr = [], lis = document.getElementById("grouplist").getElementsByClassName("user");
        for(var i=0, im=lis.length; im>i; i++)
            usr.push(lis[i].firstChild.nodeValue);
        
        //Get all selected groups
        var gr = [], lis = document.getElementById("grouplist").getElementsByClassName("group");
        for(var i=0, im=lis.length; im>i; i++)
            gr.push(lis[i].firstChild.nodeValue);

        //Get group name
        var groupname = JSON.stringify(document.getElementById("groupnameinput").value);
        var users = JSON.stringify(usr);
        var groups = JSON.stringify(gr);
        
        $.ajax({
            url: "create_group/", 
            type: "POST",
            dataType: "html",
            data: {
                'groupname': groupname,
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
