from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
                       url(r'^$', 'brodus.views.index', name='index'),
                      )
