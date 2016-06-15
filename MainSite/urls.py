from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'test/$', views.test, name='test'),
    url(r'btc/$', views.btc, name='btc'),
    url(r'solar/$', views.solar, name='solar'),
    url(r'wind/$', views.wind, name='wind'),
    url(r'dashboard1/$', views.dashboard1, name="dashboard1"),
]