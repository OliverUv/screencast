$ ->
  dom_complete_box = $("#username_input")
  dom_selected_users_list = $('#selected_users')
  dom_selected_user_column = $('#usercolumn')
  dom_selected_group_column = $('#groupcolumn')
  dom_selected_group_list = $('#selected_group')
  dom_selected_group_name = $('#group_name')
  dom_create_button = $('#create_group_button')
  dom_group_name_box = $('#groupnameinput')
  dom_result = $('#result')

  currently_selected_users = []
  past_selected_users = []
  selected_group = ''
  selected_group_members = []
  cache = {}


  select_user = (username) ->
    return if username in currently_selected_users
    currently_selected_users.push(username)
    past_selected_users.push(username)
    refresh_gui()


  deselect_user = (username) ->
    return if username not in currently_selected_users
    currently_selected_users.remove(username)
    refresh_gui()


  select_group = (group_name, group_members) ->
    return if group_name == selected_group
    selected_group = group_name
    selected_group_members = group_members
    refresh_gui()


  sorted = (usernames) ->
    return _.sortBy usernames, (uname) ->
      return uname.toUpperCase()


  refresh_gui = ->
    dom_selected_users_list.empty()
    dom_selected_group_list.empty()

    users_to_show = _.union(currently_selected_users, past_selected_users)
    users_to_show = sorted(users_to_show)

    if users_to_show == []
      dom_selected_user_column.hide()
    else
      dom_selected_user_column.show()
      for username in users_to_show
        dom_selected_users_list.append(create_username_clickable_box(username))

    if selected_group == ''
      dom_selected_group_column.hide()
    else
      dom_selected_group_name.text(selected_group)
      for username in sorted(selected_group_members)
        dom_selected_group_list.append(create_username_clickable_box(username))
      dom_selected_group_column.show()


  get_username_selection_class = (username) ->
    if username in currently_selected_users
      return "added_user"
    else
      return "non_added_user"


  get_group_selection_class = (group_name, group_members) ->
    all_members_selected = true
    any_member_selected = false
    for username in group_members
      if username in currently_selected_users
        any_member_selected = true
      else
        all_members_selected = false

    if all_members_selected
      return 'all_selected_group'
    else if any_member_selected
      return 'some_selected_group'
    else
      return 'none_selected_group'


  create_username_complete_box = (username) ->
    return $("<li class='#{get_username_selection_class(username)}'><a>#{username}</a></li>")


  create_group_complete_box = (group_name, group_members) ->
    css_selection_class = get_group_selection_class(group_name, group_members)
    return $("<li class='#{css_selection_class}'><a>#{group_name}</a></li>")


  create_username_clickable_box = (username) ->
    box = $("<li class='#{get_username_selection_class(username)}'>#{username}</li>")
    box.on 'click', ->
      if username in currently_selected_users
        deselect_user(username)
      else
        select_user(username)


  create_category_list_item = (category_name) ->
    return $("<li class='ui-autocomplete-category'>#{category_name}</li>")


  # Used to filter out already selected users from the autocomplete suggestions
  filter_selected_users = (user_group_list) ->
    _.filter user_group_list, (item) ->
      if item.category == '' and item.value in currently_selected_users
        return false
      return true


  # Subclass autocomplete widget to enable custom drawing and categories.
  $.widget "custom.user_group_complete", $.ui.autocomplete,
    _renderItem: (ul, item) ->
      if item.category == ''
        create_username_complete_box(item.value).appendTo(ul)
      else
        create_group_complete_box(item.value, item.members).appendTo(ul)
    _renderMenu: (ul, items) ->
      that = this
      current_category = ''
      for item in items
        # Divide things up into categories, assumes items are grouped by category.
        if current_category != item.category
          ul.append(create_category_list_item(item.category))
          current_category = item.category
        that._renderItemData(ul, item)


  dom_complete_box.user_group_complete
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


  dom_create_button.on "click", ->
    group_name = dom_group_name_box.val()
    if group_name?.length
      # TODO warn about empty group name
      null

    $.ajax
      url: 'create_group/'
      type: 'POST'
      dataType: 'JSON'
      data:
        groupname: group_name
        users: currently_selected_users
      success: (result) ->
        dom_result.text(result)  # TODO report things beautifully
      error: (xhr, errmsg, err) ->
        dom_result.text('ERROR: ' + xhr + errmsg + err)  # TODO report things beautifully
