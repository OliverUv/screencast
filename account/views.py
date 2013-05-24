from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.template import Context, loader, RequestContext
from django.http import Http404,HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import Resource, LazyEncoder
from guardian.shortcuts import get_objects_for_user, assign
from django.utils import simplejson

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
    resources = Resource.objects.all()
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
    #Handle submitted users to share to
    #if request.method == 'POST':
    return HttpResponseRedirect(reverse('account:profile'))

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


