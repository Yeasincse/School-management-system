from django.conf.urls import url
from . import views

urlpatterns = [
    # registration for office
    url(r'^registration/$', views.Registration.as_view(), name='registration'),

    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^logout/$', views.logout_request, name='logout'),

    # member registration by office ( universal )
    url(r'^registration-member/$', views.RegistrationMember.as_view(), name='registration-member'),

    # additional information for teacher
    url(r'^add-teacher/(?P<pk>[0-9]+)/$', views.AddTeacher.as_view(), name='add-teacher'),

    # additional information for parent
    url(r'^add-parent/(?P<pk>[0-9]+)/$', views.AddParent.as_view(), name='add-parent'),

    # additional information for school
    url(r'^add-school/(?P<pk>[0-9]+)/$', views.AddSchool.as_view(), name='add-school'),

    # additional information for student
    url(r'^add-student/(?P<pk>[0-9]+)/$', views.AddStudent.as_view(), name='add-student'),

    # additional information for librarian
    url(r'^add-librarian/(?P<pk>[0-9]+)/$', views.AddLibrarian.as_view(), name='add-librarian'),
]
