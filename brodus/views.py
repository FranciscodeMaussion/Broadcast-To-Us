from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from brodus.models import Jobs, Workers, Proj, Idioma, Lenguaje, Rol
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
    idiomas = Idioma.objects.all()
    lenguajes = Lenguaje.objects.all()
    trabajos = Jobs.objects.all()
    if request.method=='POST':
        print request.POST
        n_u=User()
        username=request.POST['username']
        n_u.username=username
        n_u.email=request.POST['email']
        password=request.POST['password1']
        rol=Rol()
        rol.nombre=username
        n_u.set_password(password)
        n_u.save()
        rol.user=n_u
        rol.save()
        ids_idioma=request.POST.getlist("idiomas")
        print ids_idioma
        for i in ids_idioma:
            print i
            aux = Idioma.objects.get(id = i)
            rol.idioma.add(aux)
        ids_lenguajes=request.POST.getlist('lenguajes')
        print ids_lenguajes
        for i in ids_lenguajes:
            aux = Lenguaje.objects.get(id = i)
            rol.lenguaje.add(aux)
        ids_trabajos=request.POST.getlist('trabajos')
        for i in ids_trabajos:
            aux = Jobs.objects.get(id = i)
            rol.trabajo.add(aux)
        user = authenticate(username=username, password=password)
        login(request, user)
    return render_to_response('a_user.html',{'idiomas':idiomas,'lenguajes':lenguajes,'trabajos':trabajos},
                              context)

@login_required(login_url='/user/log_in')
def log_out(request):
    logout(request)
    context = RequestContext(request)
    return redirect('/')
