from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import Resource
from guardian.shortcuts import get_objects_for_user, assign
from account.common import http_badrequest, http_success, ensure_post, http_json_response
import json
import models


@login_required
def index(request):
    users = User.objects.order_by('username')
    resources = Resource.objects.all()

    context = Context({
        'users': users,
        'resource_list': resources,
    })

    return render(request, 'account/index.html', context)


@login_required
def profile(request):
    resources = get_objects_for_user(request.user, 'account.view_resource')
    users = User.objects.order_by('username')
    groups = Group.objects.all()
    context = Context({
        'users': users,
        'thisuser': request.user,
        'resource_list': resources,
        'groups': groups,
    })

    return render(request, 'account/profile.html', context)


@login_required
def browse(request):
    user = request.user
    created = Resource.objects.filter(key=user)
    # Get intersection from created and owned resources
    resources = get_objects_for_user(User.objects.get(username=user.username), 'account.view_resource').exclude(key=user)
    context = Context({
        'shared_resource': resources,
        'created_resources': created,
        'thisuser': user,
    })

    return render(request, 'account/browse.html', context)


@login_required
def complete_usernames(request, partial_username):
    if (len(partial_username) < 2):
        return http_json_response([])  # Don't return anything for < 2 chars

    max_results = 20
    matching_names = User.objects.filter(username__icontains=partial_username)
    matching_names = matching_names.order_by('username').values_list('username', flat=True)
    matching_names = matching_names[:max_results]  # limit number of results
    return http_json_response(list(matching_names))


@login_required
def groups(request):
    users = User.objects.order_by('username')
    groups = Group.objects.all()

    context = Context({
        'users': users,
        'thisuser': request.user,
        'groups': groups,
    })

    return render(request, 'account/groups.html', context)


@login_required
def upload(request):
    resource, c = Resource.objects.get_or_create(key=request.user, filename=request.POST['resource'])
    assign('modify_resource', request.user, resource)
    assign('view_resource', request.user, resource)

    users = User.objects.order_by('username')
    resources = Resource.objects.all()

    context = RequestContext(request, {
        'users': users,
        'resource_list': resources,
        'uploaded': resource,
        'created': c,
    })

    return render(request, 'account/upload.html', context)


@ensure_post
@login_required
def create_group(request):
    try:
        users = request.POST.getlist('users', None)
        group_name = request.POST.get('groupname', None)
    except ValueError:
        return http_badrequest('Could not parse response.')

    if users is None or group_name is None:
        return http_badrequest('Users and group name must be specified.')

    if not group_name:
        return http_badrequest('New group must have a name.')

    try:
        users = User.objects.filter(username__in=users)
    except ObjectDoesNotExist:
        return http_badrequest('No such users exist.')

    new_group = models.create_group(group_name, request.user)

    for user in users:
        user.groups.add(new_group)

    return http_success()


@ensure_post
@login_required
def get_group(request):
    # TODO this should be a GET request, since it doesn't modify data.
    #Parse data
    jsgroup = request.POST['group']
    group = json.loads(jsgroup)
    message = ''

    #Get users
    try:
        gUsers = User.objects.filter(groups__name=group)
    except ObjectDoesNotExist:
        message = 'Groups not found'

    if len(message) == 0:
        message = 'Success'

    users = " ".join(gUsers.values_list('username', flat=True).order_by('username'))
    result = json.dumps({"users": users, "message": message})
    return HttpResponse(result, mimetype='text/json')


@ensure_post
@login_required
def share(request):
    #Parse data
    jsusernames = request.POST['users']
    jsgroupnames = request.POST['groups']
    jsresourcenames = request.POST['resources']
    usernames = json.loads(jsusernames)
    groupnames = json.loads(jsgroupnames)
    resourcenames = json.loads(jsresourcenames)
    message = ''

    #Get users, resources, groups
    try:
        message = 'Users not found'
        users = User.objects.filter(username__in=usernames)
        message = 'Resources not found'
        resources = Resource.objects.filter(filename__in=resourcenames)
        message = 'Groups not found'
        groups = Group.objects.filter(name__in=groupnames)
        message = ''
    except ObjectDoesNotExist:
        return HttpResponse(message, mimetype='application/javascript')

    #Assign access rights to users and groups
    for resource in resources:
        for user in users:
            assign('view_resource', user, resource)
        for group in groups:
            assign('view_resource', group, resource)

    message = 'Shared..'

    return HttpResponse(message, mimetype='application/javascript')


@login_required
def share_add_users(request):  # TODO Seems unused?
    if request.method == 'POST':
        files = request.POST.getlist('files')
        message = 'Worked'
        rtype = 'success'
    else:
        message = 'Something went wrong'
        rtype = 'error'

   #Build response
    result = json.dumps({
        'message': message,
        'type': rtype
    })
    return HttpResponse(result, mimetype='application/javascript')


@login_required
def launch_applet(request):
    context = Context({
        'user': request.user,
    })

    return render(request, 'account/applet.html', context)
