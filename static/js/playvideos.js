$(document).ready(function(){
    $('.videolink').on('click', function(){
        var clicked = $(event.target);
        //html = '<video id="video" controls="controls" width="640" height="360">';
        //html = ''
        //document.getElementById('videosource').innerHTML = html + '<source type="video/webm" src="{{ STATIC_URL }}media/' + clicked.attr('id') + '">';
        var myVideo = document.getElementById('video');
        $(myVideo).attr('poster', '/static/media/' + clicked.attr('id') + '.png');
        myVideo.src = '/static/media/' + clicked.attr('id') + '.webm';
        myVideo.load();
    });
});
