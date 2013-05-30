from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
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
    context = Context({
        'user': request.user,
        'resource_list': resources,
        })

    return render(request, 'account/profile.html', context)

@login_required
def browse(request):
    #resources = Resource.objects.all()
    resources = get_objects_for_user(User.objects.get(username='testpilot'), 'account.view_resource')
    context = Context({
        'resource_list': resources,
        })

    return render(request, 'account/browse.html', context)

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
def test(request):
    resources = get_objects_for_user(request.user, 'account.view_resource')
    users = User.objects.order_by('username')
    context = Context({
        'users': users,
        'thisuser': request.user,
        'resource_list': resources,
        })

    return render(request, 'account/test.html', context)

@login_required
def share(request):
    if request.method == 'POST':
        #Parse data
        jsusernames = request.POST['sharedusers']
        jsresourcenames = request.POST['resources']
        usernames = json.loads(jsusernames)
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

        #Assign access rights to users
        for user in users:
            for resource in resources:
                assign('view_resource', user, resource)

        if len(message) == 0:
            message = 'Worked'
        
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


