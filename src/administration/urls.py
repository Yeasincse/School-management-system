from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='home'),

    url(r'^add-member/$', views.AddMember.as_view(), name='add-member'),
]
