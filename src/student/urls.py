from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'dashboard/$', views.studenthome, name='index'),

    #::::start member operation module url::::
    #:::::::::::::::::::::::::::::::::::::::::

    url(r'^member/detail/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(), name='member-detail'),
    url(r'^member/edit/(?P<pk>[0-9]+)/$', views.MemberEdit.as_view(), name='member-edit'),


    #:::::::::::::::::::::::::::::::::::::::
    #::::end member operation module url::::


    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::


    url(r'^schedule/$', views.Schedule.as_view(), name='schedule'),

    #view  routine
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9-_]+)/routine/view/$', views.RoutineView.as_view(), name='routine-view'),
    #create exam routine
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/exam-routine/view/$', views.ExamRoutineView.as_view(), name='student-exam-routine-view'),


    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::

]
