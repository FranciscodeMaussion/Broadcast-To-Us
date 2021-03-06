from django.conf.urls import patterns, include, url
urlpatterns = patterns('',
                       url(r'^$', 'brodus.views.index', name='index'),
                       url(r'^user/log_in$','brodus.views.log_in', name='log_in'),
                       url(r'^user/new$','brodus.views.new_user', name='new_user'),
                       url(r'^user/log_out$','brodus.views.log_out', name='log_out'),
                       url(r'^add/new/$','brodus.views.add_new', name='add_new'),
                       url(r'^add/active/$','brodus.views.add_active', name='add_active'),
                       url(r'^proyecto/new/$','brodus.views.new_proy', name='new_proy'),
                       url(r'^proyecto/mod/(?P<proj>[0-9]+)$','brodus.views.mod_proy', name='mod_proy'),
                       url(r'^proyecto/(?P<proj>[0-9]+)$','brodus.views.show_proy', name='show_proy'),
                       url(r'^proyecto/del/(?P<proj>[0-9]+)$','brodus.views.del_proy', name='del_proy'),
                       url(r'^proyecto/create$','brodus.views.n_p', name='create_proj'),
                       url(r'^work/add/(?P<w_p>[0-9]+)$','brodus.views.n_p_w', name='add_work'),
                       url(r'^work/del/(?P<w_p>[0-9]+)$','brodus.views.d_p_w', name='del_work'),
                       url(r'^channel/$','brodus.views.channel', name='channel'),
                      )
#url(r'^proyecto/participar/(?P<proj>[0-9]+)$','brodus.views.part_proy', name='part_proy'),
