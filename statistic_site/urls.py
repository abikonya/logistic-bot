from django.conf.urls import url
from statistic_site import views

app_name = 'statistic_site'

urlpatterns = [
    url(r'^$', views.MainView.as_view(), name='main'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
]