from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from brodus.models import Jobs, Workers, Proj, Idioma, Lenguaje, Rol
from django.conf import settings
# Create your views here.

@login_required()
def index(request):
    context = RequestContext(request)
    rol_user = Rol.objects.get(user = request.user)
    return render_to_response('index.html',
                              {'rol_user':rol_user},
                              context)

@login_required()
def new_proy(request):
    context = RequestContext(request)
    rol_user = Rol.objects.get(user = request.user)
    return render_to_response('n_proj.html',
                              {'rol_user':rol_user},
                              context)

@login_required()
def mod_proy(request, proj):
    context = RequestContext(request)
    proj = Proj.objects.get(id = proj)
    if request.method=='POST':
        print request.POST
        proj.nombre = request.POST['name']
        proj.desc = request.POST['desc_proy']
        proj.save()
        p_i = request.POST.getlist("idiomas")
        proj.nescesita_i.clear()
        for i in p_i:
            aux = Idioma.objects.get(id = i)
            proj.nescesita_i.add(aux)
        p_l = request.POST.getlist("lenguajes")
        proj.nescesita_l.clear()
        for i in p_l:
            aux = Lenguaje.objects.get(id = i)
            proj.nescesita_l.add(aux)
        return redirect('/')
    else:
        idiomas = Idioma.objects.all()
        lenguajes = Lenguaje.objects.all()
        trabajos = Jobs.objects.all()
        rol_user = Rol.objects.get(user = request.user)
        return render_to_response('m_proj.html',
                                  {'idiomas':idiomas,
                                   'lenguajes':lenguajes,
                                   'trabajos':trabajos,
                                   'proj':proj,
                                   'works':proj.nescesita_w,
                                  'rol_user':rol_user},
                                  context)

@login_required()
def n_p(request):
    if request.method=='POST':
        name = request.POST['name']
        desc = request.POST['desc_proy']
        proy = Proj()
        proy.nombre = name
        proy.desc = desc
        proy.owner = request.user
        proy.save()
        path = "/mod/proyecto/"+str(proy.id)#ID aca!!!!
        return redirect(path)
    return HttpResponse(status=203)

@login_required()
def n_p_w(request, w_p):
    context = RequestContext(request)
    id_t=request.POST['trab']
    cant_t=request.POST['cant']
    print cant_t
    work = Workers()
    work.tipo = Jobs.objects.get(id = id_t)
    work.cantidad = cant_t
    proj = Proj.objects.get(id = w_p)
    a = False
    for i in proj.nescesita_w.all():
        if i.tipo == work.tipo:
            i.cantidad = int(work.cantidad) + int(i.cantidad)
            i.save()
            a = True
            break
    if a == False:
        work.save()
        proj.nescesita_w.add(work)
    works = proj.nescesita_w
    return render_to_response('n_work.html',
                              {'works':works},
                              context)

@requires_csrf_token
def log_in(request):
    context = RequestContext(request)
    n = "/"
    if request.GET:
        n = request.GET['next']
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        n = request.POST['next']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(n)
            else:
                return HttpResponse(status=203)
        else:
             return HttpResponse(status=203)
    else:
         return render_to_response('log_in_user.html',
                                    {'next':n},
                                   context)

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
    return render_to_response('a_user.html',
                              {'idiomas':idiomas,
                               'lenguajes':lenguajes,
                               'trabajos':trabajos},
                              context)

@login_required()
def log_out(request):
    logout(request)
    context = RequestContext(request)
    return redirect('/')

@login_required()
def add_lenguaje(request):
    context = RequestContext(request)
    if request.method=='POST':
        l=Lenguaje()
        l.nombre=request.POST['nombre_lenguaje']
        l.save()
    return HttpResponse(status=202)

@login_required()
def add_idioma(request):
    context = RequestContext(request)
    if request.method=='POST':
        i=Idioma()
        i.nombre=request.POST['nombre_idioma']
        i.save()
    return HttpResponse(status=202)

@login_required()
def add_trabajo(request):
    context = RequestContext(request)
    if request.method=='POST':
        t=Jobs()
        t.nombre=request.POST['nombre_trabajo']
        t.desc=request.POST['desc_trabajo']
        t.save()
    return HttpResponse(status=202)
