$ ->
  dom_complete_box = $("#username_input")
  dom_selected_users_list = $('#selected_users')
  dom_selected_user_column = $('#usercolumn')
  dom_selected_group_column = $('#groupcolumn')
  dom_selected_group_list = $('#selected_group')
  dom_selected_group_name = $('#group_name')
  selected_users = []
  selected_group = ''
  selected_group_members = []


  filter_selected_users = (user_group_list) ->
    user_group_list.filter((item) ->
      if item.category == '' and item.value in selected_users
        return false
      return true)


  refresh_gui = () ->
    dom_selected_users_list.empty()
    for username in selected_users
      dom_selected_users_list.append($("<li class='added_user'>#{username}</li>"))
    dom_selected_group_list.empty()

    if selected_group == ''
      dom_selected_group_column.hide()
    else
      dom_selected_group_name.text(selected_group)
      for username in selected_group_members
        dom_selected_group_list.append(create_username_box(username))
      dom_selected_group_column.show()


  select_user = (username) ->
    return if username in selected_users
    selected_users.push(username)
    refresh_gui()


  select_group = (group_name, group_members) ->
    return if group_name == selected_group
    selected_group = group_name
    selected_group_members = group_members
    refresh_gui()


  create_username_box = (username) ->
    box_class = "non_added_user"
    box_class = "added_user" if username in selected_users
    return $("<li class='#{box_class}'><a>#{username}</a></li>")


  create_group_box = (group_name, group_members) ->
    all_members_selected = true
    any_member_selected = false
    for username in group_members
      if username in selected_users
        any_member_selected = true
      else
        all_members_selected = false

    if all_members_selected
      return $("<li class='all_selected_group'><a>#{group_name}</a></li>")
    else if any_member_selected
      return $("<li class='some_selected_group'><a>#{group_name}</a></li>")
    else
      return $("<li class='none_selected_group'><a>#{group_name}</a></li>")


  create_category_list_item = (category_name) ->
    return $("<li class='ui-autocomplete-category'>#{category_name}</li>")


  # Subclass autocomplete widget to enable custom drawing and categories.
  $.widget("custom.user_group_complete", $.ui.autocomplete, {
    _renderItem: (ul, item) ->
      if item.category == ''
        create_username_box(item.value).appendTo(ul)
      else
        create_group_box(item.value, item.members).appendTo(ul)
    _renderMenu: (ul, items) ->
      that = this
      current_category = ''
      for item in items
        # Divide things up into categories, assumes items are grouped by category.
        if current_category != item.category
          ul.append(create_category_list_item(item.category))
          current_category = item.category
        that._renderItemData(ul, item)
  })

  cache = {}

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
