$ ->
  #Menu 
  $('.btn-group > .btn').click(->
    #Change this to fit your button
    toggle = 'btn-primary'

    if $(this).hasClass(toggle)
      $(this).removeClass(toggle)
    else
      $(this).addClass(toggle)
  )

  #Edit resource
  currentFilename = '' #Track resource that is being edited
  edit = () ->
    vlink = $(this).parent().children('.videolink')
    fname = vlink.html()
    if fname.substring(0,6) != "<input"
      currentFilename = fname
      vlink.html('<input type="text" class="editbox" autofocus="true" placeholder="'+fname+'">')
  $('.editbutton').click(edit)

  $(document).on('keypress', '.editbox', (event) ->
    if event.which == 13 or event.keycode == 13
      #$(this).parent().html(this.value)
      $target = $(this).parent()
      $.ajax({
        url:'change_name/',
        type: 'POST',
        dataType: 'json',
        data: {
          'filename': currentFilename,
          'newname': this.value,
        },
        success: (json) ->
          $target.html(json.response)
        error: (xhr,json) ->
          alert(xhr.status+ '. Info: '+json.error)
          #alert(xhr.status+': '+ xhr.responseText +'\n Additional info: '+json.error)
      })
      event.preventDefault())

  #Remove resource
  remove = () ->
    #Dialog box: confirm removal
    target = $(this).parent()
    fname = target.children('.videolink').html()
    target.parent().parent().remove()
    $.ajax({
      url:'remove_resource/',
      type: 'POST',
      dataType: 'json',
      data: {
        'filename': fname,
      },
      success: (json) ->
        $('#result').append('<li>'+json.response+'</li>')
      error: (xhr,json) ->
        alert(xhr.status+ '. Info: '+json.error)
    })
  $('.removebutton').click(remove)
      
  #Play video
  $('.videolink').on('click', () ->
      clicked = $(event.target)
      myVideo = document.getElementById('video')
      $(myVideo).attr('poster', '/static/media/' + clicked.attr('id') + '.png')
      myVideo.src = '/static/media/' + clicked.attr('id') + '.webm'
      myVideo.load()
  )
