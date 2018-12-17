from django.conf.urls import url

from App import views

urlpatterns = [
    url(r'^home/', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^sl/', views.s_l, name='s_l'),
    url(r'^slc/', views.s_l_c, name='s_l_c'),
    url(r'^register/', views.register, name='register'),
    url(r'^ui/', views.u_i, name='u_i'),
    url(r'^collect/', views.collect, name='collect'),
]