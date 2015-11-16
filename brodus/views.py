from django.shortcuts import render
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponse
# Create your views here.

def index(request):
    context = RequestContext(request)
    return render_to_response('index.html', context)
