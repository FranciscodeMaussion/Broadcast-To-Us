from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
                       url(r'^$', 'brodus.views.index', name='index'),
                       url(r'^user/log_in$','brodus.views.log_in', name='log_in'),
                       url(r'^user/new$','brodus.views.new_user', name='new_user'),
                      )
