$ ->
  #Define window for global variables/functions
  root = this
  
  #Get resources from template
  root.resources = []
  root.load_resources = () ->
    root.resources = []
    resources = document.getElementsByClassName('resource_storage')
    for resource in resources
      root.resources.push($(resource).html())
  root.load_resources()

  #Load button values (checked<1> or unchecked<0>)
  root.checked_btns = new Array()
  load_btn_values = () ->
    $('.btn-group > div').each(() ->
      if $(this).hasClass('btn-primary')
        root.checked_btns[this.id] = 1)
  load_btn_values()

  #Search
  $(document).on('keyup', '#searchfield', (event) ->
    word = this.value
    $.each(root.resources, () ->
      $this = $('#'+this)
      btn = $this.attr('class').split('_')[0]+'_btn'
      if str_contains(this, word)
        $this.removeClass('no_match')
      else
        $this.addClass('no_match')

      if not $this.hasClass('no_match') and root.checked_btns[btn]
        $this.show()
      else
        $this.hide()
    )
  )
  str_contains = (str,word) -> return str.indexOf(word) != -1

  #Toggle filter buttons
  $('.btn-group > .btn').click(->
    #Change this to fit your button
    toggle = 'btn-primary'
    selected_btn = $(this).attr('id')
    if $(this).hasClass(toggle)
      #Unchecked
      $(this).removeClass(toggle)
      root.checked_btns[selected_btn] = 0
      if selected_btn == 'created_btn'
        $('.created_resource').hide()
      else
        $('.shared_resource').hide()
    else
      #Checked
      $(this).addClass(toggle)
      root.checked_btns[selected_btn] = 1
      if selected_btn == 'created_btn'
        $('.created_resource:not(.no_match)').show()
      else
        $('.shared_resource:not(.no_match)').show()
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

  update_videolist_element = (name, new_name, $target) ->
    $target.html(new_name)
    resource_store = $('#'+name+'> .resource_storage').html(this.value)


  $(document).on('keypress', '.editbox', (event) ->
    if event.which == 13 or event.keycode == 13
      $target = $(this).parent()
      $storage = $(this).parent().parent().parent().parent().siblings('.resource_storage')
      new_name = this.value
      $.ajax({
        url: window.change_name_URL,
        type: 'POST',
        dataType: 'json',
        data: {
          'filename': currentFilename,
          'newname': new_name,
        },
        success: (json) ->
          #TODO: Low priority: Place resource name in the right index (order alphabetical)
          $target.siblings('.errormsg').html('')
          $target.html(json.message)
          $storage.html(json.message)                #set new name for li-element
          $storage.parent().attr('id', json.message) #set new name for li-element
          root.load_resources()
        error: (xhr,json) ->
          $target.siblings('.errormsg').html(errorMessage(xhr))
      })
      event.preventDefault())

  #Remove resource
  remove = () ->
    #TODO Dialog box: confirm removal
    target = $(this).parent()
    fname = target.children('.videolink').html()
    target.parent().parent().remove()
    $.ajax({
      url: window.remove_resource_URL,
      type: 'POST',
      dataType: 'json',
      data: {
        'filename': fname,
      },
      success: (json) ->
        $('#result').append('<li>'+json.response+'</li>')
      error: (xhr) ->
        $target.siblings('.errormsg').html(errorMessage(xhr))
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
