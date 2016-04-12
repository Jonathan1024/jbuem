from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'test/$', views.test, name='test'),
    url(r'btc/$', views.btc, name='btc'),
    url(r'solar/$', views.solar, name='solar'),
    url(r'wind/$', views.wind, name='wind'),
    url(r'historical/$', views.historical, name='historical'),
    url(r'about/$', views.about, name='about'),
]