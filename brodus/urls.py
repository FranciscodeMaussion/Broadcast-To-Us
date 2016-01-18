from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
                       url(r'^$', 'brodus.views.index', name='index'),
                       url(r'^user/log_in$','brodus.views.log_in', name='log_in'),
                       url(r'^user/new$','brodus.views.new_user', name='new_user'),
                       url(r'^user/log_out$','brodus.views.log_out', name='log_out'),
                       url(r'^add/idioma$','brodus.views.add_idioma', name='add_idioma'),
                       url(r'^add/trabajo$','brodus.views.add_trabajo', name='add_trabajo'),
                       url(r'^add/lenguaje$','brodus.views.add_lenguaje', name='add_lenguaje'),
                       url(r'^new/proyecto$','brodus.views.new_proy', name='new_proy'),
                       url(r'^add/work$','brodus.views.n_p_w', name='add_work'),
                       url(r'^create/proj$','brodus.views.n_p', name='create_proj'),
                      )
