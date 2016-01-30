from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import requires_csrf_token
from brodus.models import Jobs, Workers, Proj, Idioma, Lenguaje, Rol
from django.conf import settings
from omnibus.factories import websocket_connection_factory
from omnibus.api import publish
from django.template.loader import get_template
# Create your views here.

def compare(tags1, tags2):
    for key1 in tags1:
        if key1 in tags2:
            return  True
    return False

"""a=[]
else :
a.append(key1)
print key1 , " de " , tags1 , " / " , tags2 , " = " , a
return a"""

def discover(proj,rol_user):
    if compare(proj.nescesita_l.all(),rol_user.lenguaje.all()):
        if compare(proj.nescesita_i.all(),rol_user.idioma.all()):
            for key1 in proj.nescesita_w.all():
                if key1.tipo in rol_user.trabajo.all():
                    return True
    return False

def su(request):
    rol_user = Rol.objects.get(user = request.user)
    if rol_user.su:
        return True
    return False

def perm(request, per):
    if per == request.user or su(request):
        return True
    return False

@login_required()
def channel(request):
    context = RequestContext(request)
    rol_user = Rol.objects.get(user = request.user)
    if request.method=='POST':
        proj = Proj.objects.get(id = request.POST['id_proy'])
        if discover(proj,rol_user):
            rol_user.proj_user.add(proj)
        else:
            rol_user.proj_user.remove(proj)
    return render_to_response('proj_user.html',
                          {'rol_user':rol_user},
                          context)

@login_required()
def index(request):
    context = RequestContext(request)
    rol_user = Rol.objects.get(user = request.user)
    projects = Proj.objects.all()
    print rol_user
    print rol_user.proj_user.all()
    a=[]
    for key1 in projects:
        if not key1 in rol_user.proj_user.all():
            a.append(key1)
    print a
    if a != []:
        for proj in a:
            if discover(proj,rol_user):
                rol_user.proj_user.add(proj)
    if su(request):
        idiomas = Idioma.objects.filter(active = False)
        lenguajes = Lenguaje.objects.filter(active = False)
        trabajos = Jobs.objects.filter(active = False)
        return render_to_response('index.html',
                          {'idiomas':idiomas,
                           'lenguajes':lenguajes,
                           'trabajos':trabajos,
                           'rol_user':rol_user},
                                  context)
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
    if perm(request, proj.owner) and request.method=='POST':
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
        for i in proj.rol_set.all():
            rol_user = Rol.objects.get(id = i.id)
            if proj in rol_user.proj_user.all():
                if discover(proj,rol_user):
                    rol_user.proj_user.add(proj)
                else:
                    rol_user.proj_user.remove(proj)
            else:
                if discover(proj,rol_user):
                    rol_user.proj_user.add(proj)
        publish(
            'proy',
            'reload',
            {"id_proy":proj.id},
            sender='server'  # sender id of the event, can be None.
        )
        return redirect('/')
    idiomas = Idioma.objects.filter(active = True)
    lenguajes = Lenguaje.objects.filter(active = True)
    trabajos = Jobs.objects.filter(active = True)
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
def del_proy(request, proj):
    context = RequestContext(request)
    proj = Proj.objects.get(id = proj)
    if perm(request, proj.owner):
        proj.delete()
    return redirect('/')

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
    proj = Proj.objects.get(id = w_p)
    if perm(request, proj.owner):
        id_t=request.POST['trab']
        cant_t=request.POST['cant']
        print cant_t
        work = Workers()
        work.tipo = Jobs.objects.get(id = id_t)
        work.cantidad = cant_t
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

@login_required()
def d_p_w(request, w_p):
    context = RequestContext(request)
    proj = Proj.objects.get(id = w_p)
    if perm(request, proj.owner):
        id_t=request.POST['id_w']
        work = Workers.objects.get(id = id_t)
        proj.nescesita_w.remove(work)
        if work.proj_set.all() == []:
            work.delete()
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
    idiomas = Idioma.objects.filter(active = True)
    lenguajes = Lenguaje.objects.filter(active = True)
    trabajos = Jobs.objects.filter(active = True)
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
def add_new(request):
    context = RequestContext(request)
    if request.method=='POST':
        n = eval(request.POST['tipo_new'])
        n.nombre=request.POST['nombre_new']
        n.desc=request.POST['desc_new']
        if su(request):
            n.active = True
        n.save()
    return HttpResponse(status=202)

@login_required()
def add_active(request):
    context = RequestContext(request)
    if request.method=='POST' and su(request):
        tipo_a = request.POST['tipo']
        id_a = request.POST['id']
        print id_a, tipo_a
        pos = {"Idioma":Idioma,"Lenguaje":Lenguaje,"Jobs":Jobs}
        sender = {"Idioma":'idiomas',"Lenguaje":'lenguajes',"Jobs":'trabajos'}
        pager = {"Idioma":'obj_i.html',"Lenguaje":'obj_l.html',"Jobs":'obj_t.html'}
        aux = tipo_a + ".objects.get(id = "+ id_a + ")"
        print aux
        obj = eval(aux, pos)
        print obj
        if request.POST['tDo']=="True":
            obj.active = True
            obj.save()
        else:
            obj.delete()
        aux = tipo_a + ".objects.filter(active = False)"
        objs = eval(aux, pos)
        return render_to_response(pager[tipo_a],
                              {sender[tipo_a]:objs},
                              context)
