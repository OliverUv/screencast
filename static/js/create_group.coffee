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

  create_suggestion_item = (username) ->
    box_class = "non_added_user"
    box_class = "added_user" if username in selected_users
    return $("<li class='#{box_class}'><a>#{username}</a></li>")

  create_category_item = (category_name) ->
    return $("<li class='ui-autocomplete-category'>#{category_name}</li>")

  # Subclass autocomplete widget to enable custom drawing and categories.
  $.widget("custom.user_group_complete", $.ui.autocomplete, {
    _renderItem: (ul, item) ->
      create_suggestion_item(item.value).appendTo(ul)
    _renderMenu: (ul, items) ->
      that = this
      current_category = ''
      for item in items
        if current_category != item.category
          ul.append(create_category_item(item.category))
          current_category = item.category
        that._renderItemData(ul, item)
  })

  cache = {}

  dom_complete_box.bind("keydown", (event) ->
    if event.keyCode == $.ui.keyCode.ENTER
      add_to_selected_users($(this).val())
      event.preventDefault())

  dom_complete_box.user_group_complete({
    source: (request, response) ->
      search_string = request.term
      if search_string of cache
        return response(cache[search_string])
      $.getJSON(
        "/account/complete_users_and_groups/#{request.term}"
        (data, status, xhr) ->
          cache[search_string] = data
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
