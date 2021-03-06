from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', auth_views.login, {'template_name': 'authcp/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', views.register_user, name='register'),
    url(r'^register-activate/(?P<key>.+)$', views.activation, name='register-activate'),
    url(r'^register-success/$', views.register_success, name='register-success'),
]
