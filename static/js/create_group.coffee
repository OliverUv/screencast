$ ->
  dom_complete_box = $("#username_input")
  dom_selected_list = $('#selected_users')
  selected_users = []

  add_to_selected_users = (username) ->
    return if username in selected_users
    selected_users.push(username)
    update_user_selection()

  update_user_selection = () ->
    dom_selected_list.empty()
    for username in selected_users
      dom_selected_list.append($("<li class='added_user'>#{username}</li>"))

  create_suggestion_box = (username) ->
    box_class = "non_added_user"
    box_class = "added_user" if username in selected_users
    return $("<li class='#{box_class}'><a>#{username}</a></li>")


  cache = {}

  dom_complete_box.bind("keydown", (event) ->
    if event.keyCode == $.ui.keyCode.ENTER
      add_to_selected_users($(this).val())
      event.preventDefault())

  dom_complete_box.autocomplete({
    source: (request, response) ->
      partial_username = request.term
      if partial_username of cache
        return response(cache[partial_username])
      $.getJSON(
        "/account/complete_usernames/#{request.term}"
        (data, status, xhr) ->
          cache[partial_username] = data
          response(data))
    minLength: 2
    select: (event, ui) ->
      if ui.item?
        add_to_selected_users(ui.item.value)
        event.preventDefault()
      else
        alert "Nothing selected, input was #{this.value}"
        event.preventDefault()
  })

  # Manual styling for autocomplete items
  dom_complete_box.data("ui-autocomplete")._renderItem = (ul, item) ->
    create_suggestion_box(item.value).appendTo(ul)
