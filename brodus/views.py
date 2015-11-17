from django.shortcuts import render
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
# Create your views here.

def index(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)

@requires_csrf_token
def log_in(request):
    context = RequestContext(request)
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse(status=202)
            else:
                return HttpResponse(status=203)
        else:
             return HttpResponse(status=203)
    else:
         return render_to_response('log_in_user.html', context)

@requires_csrf_token
def new_user(request):
    context = RequestContext(request)
    if request.method=='POST':
        n_u=User()
        username=request.POST['username']
        n_u.username=username
        n_u.email=request.POST['email']
        password=request.POST['password']
        n_u.set_password(password)
        n_u.save()
        user = authenticate(username=username, password=password)
        login(request, user)
    return render_to_response('a_user.html',
                              context)

@login_required(login_url='/user/log_in')
def log_out(request):
    logout(request)
    context = RequestContext(request)
    return redirect('/')
