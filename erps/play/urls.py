from django.conf.urls import patterns, url

from play import views

urlpatterns = patterns('',
    url(r'^create/$', views.create, name='create'),
    url(r'^get/$', views.get, name='get'),
    url(r'^show_groups/$', views.show_groups, name='show_groups'),
    url(r'^show/$', views.show, name='show'),
    url('', views.welcome, name='welcome'),


)