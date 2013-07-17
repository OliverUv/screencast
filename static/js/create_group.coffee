$ ->
  dom_complete_box = $("#username_input")
  dom_selected_users_list = $('#selected_users')
  dom_selected_group_list = $('#selected_group')
  selected_users = []
  selected_group = ''
  selected_group_members = []

  filter_selected_users = (user_group_list) ->
    user_group_list.filter((item) ->
      if item.category == '' and item.value in selected_users
        return false
      return true)

  update_selected_users = () ->
    dom_selected_users_list.empty()
    for username in selected_users
      dom_selected_users_list.append($("<li class='added_user'>#{username}</li>"))
    dom_selected_group_list.empty()
    if select_group != ''
      dom_selected_group_list.append($("<li class='selected_group_header'>#{selected_group}</li>"))
      for username in selected_group_members
        dom_selected_group_list.append(create_suggestion_item(username))

  select_user = (username) ->
    return if username in selected_users
    selected_users.push(username)
    update_selected_users()

  select_group = (group_name, group_members) ->
    return if group_name == selected_group
    selected_group = group_name
    selected_group_members = group_members
    update_selected_users()

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
        # Divide things up into categories, assumes items are grouped by category.
        if current_category != item.category
          ul.append(create_category_item(item.category))
          current_category = item.category
        that._renderItemData(ul, item)
  })

  cache = {}

  dom_complete_box.bind("keydown", (event) ->
    if event.keyCode == $.ui.keyCode.ENTER
      select_user($(this).val())
      event.preventDefault())

  dom_complete_box.user_group_complete({
    source: (request, response) ->
      search_string = request.term
      if search_string of cache
        return response(filter_selected_users(cache[search_string]))
      $.getJSON(
        "/account/complete_users_and_groups/#{request.term}"
        (data, status, xhr) ->
          cache[search_string] = data
          response(filter_selected_users(data)))
    minLength: 2
    select: (event, ui) ->
      if ui.item?
        if ui.item.category == ''
          select_user(ui.item.value)
        else if ui.item.category == 'groups'
          select_group(ui.item.value, ui.item.members)
      dom_complete_box.val('')  # Clear input field
      # Return false to inhibit insertion of the selected value
      # into the input field.
      return false
  })
