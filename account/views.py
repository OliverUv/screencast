from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.template import Context, RequestContext
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import Resource
from guardian.shortcuts import get_objects_for_user, assign
from account.common import http_badrequest, http_success, ensure_post, http_json_response
from hashlib import sha224
import json
import models
import datetime


def login(request):
    context = Context({})
    return render(request, 'account/login.html', context)


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
def my_files(request):
    user = request.user
    # Get intersection from created and owned resources
    shared_resources = get_objects_for_user(User.objects.get(username=user.username), 'account.view_resource').exclude(key=user)
    # Get all resources for user
    owned_resources = get_objects_for_user(User.objects.get(username=user.username), 'account.view_resource').order_by('upload_date')
    # Mark the resources shared by other users
    for resource in owned_resources:
        if resource in shared_resources:
            resource.is_shared = True
        else:
            resource.is_shared = False

    context = RequestContext(request, {
        'resources': owned_resources,
    })
    return render(request, 'account/my_files.html', context)


@login_required
def player(request):
    user = request.user
    # Get intersection from created and owned resources
    shared_resources = get_objects_for_user(User.objects.get(username=user.username), 'account.view_resource').exclude(key=user)
    # Get all resources for user
    owned_resources = get_objects_for_user(User.objects.get(username=user.username), 'account.view_resource').order_by('upload_date')
    # Mark the resources shared by other users
    for resource in owned_resources:
        if resource in shared_resources:
            resource.is_shared = True
        else:
            resource.is_shared = False

    context = RequestContext(request, {
        'resources': owned_resources,
    })
    return render(request, 'account/player.html', context)


#TODO Testa change name och remove resource med resurser som har olika anvandare
@login_required
def change_name(request):
    res = ''
    if request.method == 'POST':
        if Resource.objects.filter(disp_name=request.POST['newname']).exists():
            return http_badrequest('Name is not unique')
        else:
            try:
                resource = Resource.objects.get(disp_name=request.POST['filename'])
                user = User.objects.get(username=request.user)
                if user.has_perm('modify_resource', resource):
                    resource.disp_name = request.POST['newname']
                    resource.save()
                    res = request.POST['newname']
                else:
                    return http_badrequest('Permission denied')
            except ObjectDoesNotExist:
                return http_badrequest('Object does not exist')
    else:
        http_badrequest('Request is not a POST')

    result = {'message': res}
    return http_json_response(result)


@login_required
def remove_resource(request):
    res = ''
    if request.method == 'POST':
        try:
            resource = Resource.objects.get(disp_name=request.POST['filename'])
            user = User.objects.get(username=request.user)
            if user.has_perm('modify_resource', resource):
                resource.delete()
                res = request.POST['filename'] + ' sucessfully deleted'
                return http_json_response(res)
            else:
                return http_badrequest('Permission denied')
        except ObjectDoesNotExist:
            return http_badrqeuest('Object does not exist')
    else:
        return http_badrequest('Request is not a POST')
    result = {'message': res}
    return http_json_response(result)


@login_required
def complete_users_and_groups(request, completion_string):
    if (len(completion_string) < 2):
        return http_json_response([])  # Don't return anything for < 2 chars

    max_results = 20
    matching_names = User.objects.filter(username__icontains=completion_string)
    matching_names = matching_names.order_by('username').values_list('username', flat=True)
    matching_names = matching_names[:max_results / 2]  # limit number of results
    matching_names = list(matching_names)
    users = [{'value': n, 'category': ''} for n in matching_names]

    matching_groups = Group.objects.filter(
        name__icontains=completion_string,
        observers=request.user
    ).prefetch_related('user_set')  # Prefetch the members of each group
    matching_groups = matching_groups.order_by('name')
    matching_groups = matching_groups[:max_results / 2]
    groups = [{
        'value': g.name,
        'category': 'groups',
        'members': [u.username for u in g.user_set.all()]}
        for g in matching_groups]

    return http_json_response(users + groups)


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
def create_cast(request):
    display_name = request.POST['resource']
    cast_uuid = sha224(request.user.username + display_name + str(datetime.datetime.now().time())).hexdigest()

    resource, c = Resource.objects.get_or_create(
        key=request.user,
        cast_uuid=cast_uuid,
        filename=display_name,
        disp_name=display_name)
    assign('modify_resource', request.user, resource)
    assign('view_resource', request.user, resource)

    users = User.objects.order_by('username')
    resources = Resource.objects.all()

    context = RequestContext(request, {
        'users': users,
        'resource_list': resources,
        'uploaded': resource,
        'created': c,
        'connect_settings': {
            'host': settings.IDACAST_HOST,
            'port': settings.IDACAST_PORT,
            'user_id': request.user.username,
            'cast_uuid': cast_uuid,
            'upload_token': request.user.profile.upload_token
        }
    })

    # TODO update part of the current page instad of loading new page
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
