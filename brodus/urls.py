from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
                       url(r'^$', 'brodus.views.index', name='index'),
                       url(r'^user/log_in$','brodus.views.log_in', name='log_in'),
                      )
