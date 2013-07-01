from django.core.urlresolvers import reverse
from django.contrib.auth.models import User,Group
from django.template import Context, loader, RequestContext
from django.http import Http404,HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import Resource, LazyEncoder
from guardian.shortcuts import get_objects_for_user, assign
from django.utils import simplejson
import json

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
    #Get intersection from created and owned resources
    resources = get_objects_for_user(User.objects.get(username=user.username), 'account.view_resource').exclude(key=user)
    context = Context({
        'shared_resource': resources,
        'created_resources':created,
        'thisuser': user,
        })

    return render(request, 'account/browse.html', context)

@login_required
def test(request):
    users = User.objects.order_by('username')
    groups = Group.objects.all()

    context = Context({
        'users': users,
        'thisuser': request.user,
        'groups': groups,
        })

    return render(request, 'account/test.html', context)

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

@login_required
def create_group(request):
    if request.method == 'POST':
        #Parse data
        jsgroupname = request.POST['groupname']
        jsusernames = request.POST['users']
        jsgroupnames = request.POST['groups']
        usernames = json.loads(jsusernames)
        groupnames = json.loads(jsgroupnames)
        gName = json.loads(jsgroupname)
        message = '' 
        
        #Create group
        newGroup = Group(name=gName)
        newGroup.save()

        #Get users
        try:
            users = User.objects.filter(username__in=usernames)
        except ObjectDoesNotExist:
            message = 'Users not found'

        try:
            gUsers = User.objects.filter(groups__name__in=groupnames)
        except ObjectDoesNotExist:
            message = 'Groups not found'

        #Merge querysets and add group
        allusers = gUsers | users        
        for user in allusers:
            user.groups.add(newGroup)

        if len(message) == 0:
            message = 'Created..'

         #PRINT USERS
         #message = str(allusers.values_list('username'))
    else:
        message = 'Not a POST'

    #Build response
    result = simplejson.dumps({
        'message': message,
    },cls=LazyEncoder)
  
    return HttpResponse(message, mimetype='application/javascript')

@login_required
def get_group(request):
    if request.method == "POST":
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

    else:
        message = 'Not a POST'

    users = " ".join(gUsers.values_list('username',flat=True).order_by('username')) 
    result = json.dumps({"users": users, "message": message})
    return HttpResponse(result, mimetype='application/javascript')

@login_required
def share(request):
    if request.method == 'POST':
        #Parse data
        jsusernames = request.POST['users']
        jsgroupnames = request.POST['groups']
        jsresourcenames = request.POST['resources']
        usernames = json.loads(jsusernames)
        groupnames = json.loads(jsgroupnames)
        resourcenames = json.loads(jsresourcenames)
        message = '' 

        #Get users
        try:
            users = User.objects.filter(username__in=usernames)
        except ObjectDoesNotExist:
            message = 'Users not found'

        #Get resources
        try:
            resources = Resource.objects.filter(filename__in=resourcenames)
        except ObjectDoesNotExist:
            message = 'Resources not found'

        #Get groups 
        try:
            groups = Group.objects.filter(name__in=groupnames)
        except ObjectDoesNotExist:
            message = 'Groups not found'

        #Assign access rights to users and groups
        for resource in resources:
            for user in users:
                assign('view_resource', user, resource)
            for group in groups:
                assign('view_resource', group, resource)

        if len(message) == 0:
            message = 'Shared..'
        
    else:
        message = 'Something went wrong'

    #Build response
    result = simplejson.dumps({
        'message': message,
    },cls=LazyEncoder)
  
    return HttpResponse(message, mimetype='application/javascript')

@login_required
def share_add_users(request):
    if request.method == 'POST':
        files = request.POST.getlist('files')
        message = 'Worked'
        rtype = 'success'
    else:
        message = 'Something went wrong'
        rtype = 'error'

   #Build response
    result = simplejson.dumps({
        'message': message,
        'type': rtype
    },cls=LazyEncoder)
    return HttpResponse(result, mimetype='application/javascript')


@login_required
def launch_applet(request):
    context = Context({
        'user': request.user,
        })

    return render(request, 'account/applet.html', context)
