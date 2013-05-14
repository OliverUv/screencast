from django.conf.urls import patterns, url
from django.contrib.auth.models import User
from django.template import Context, loader, RequestContext
from django.http import Http404,HttpResponse, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from models import Resource
from guardian.shortcuts import get_objects_for_user, assign
#from django.core.urlresolvers import reverse
#from django.views.generic import DetailView, ListView
#from django.core.context_processors import csrf

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
