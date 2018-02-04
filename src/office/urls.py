from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Home.as_view(), name='index'),

    #::::start member operation module url::::
    #:::::::::::::::::::::::::::::::::::::::::

    url(r'^office-registration/$', views.Registration.as_view(), name='office-registration'),

    #member operations
    url(r'^member/search/$', views.MemberSearch.as_view(), name='member-search'),

    #list of member
    url(r'^member/list/$', views.MemberList.as_view(), name='member-list'),
    url(r'^member/list/(?P<type>[a-zA-Z]+)/$', views.MemberListDetail.as_view(), name='member-list-detail'),

    #list of class in student
    url(r'^member/list/student/class/$', views.StudentClass.as_view(), name='student-class'),
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/$', views.StudenListInClass.as_view(), name='student-list-in-class'),

    #list of section in class
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/section/$', views.ClassWiseSection.as_view(), name='section'),
    url(r'^member/list/student/class/(?P<classes>[a-zA-Z0-9]+)/section/(?P<section>[a-zA-Z0-9-_]+)/$', views.SectionWiseStudent.as_view(), name='section-wise-student'),

    url(r'^member/detail/(?P<pk>[0-9]+)/$', views.MemberDetail.as_view(), name='member-detail'),
    url(r'^member/edit/(?P<pk>[0-9]+)/$', views.MemberEdit.as_view(), name='member-edit'),
    url(r'^member/delete/(?P<pk>[0-9]+)/$', views.MemberDelete.as_view(), name='member-delete'),

    #:::::::::::::::::::::::::::::::::::::::
    #::::end member operation module url::::


    #::::start schedule module url::::
    #:::::::::::::::::::::::::::::::::


    url(r'^schedule/$', views.Schedule.as_view(), name='schedule'),
    url(r'^schedule/class-list/$', views.ClassList.as_view(), name='class-list'),
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/$', views.SectionList.as_view(), name='section-list'),

    #create routine
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9-_]+)/routine/create/$', views.RoutineCreate.as_view(), name='routine-create'),
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/(?P<section>[a-zA-Z0-9-_]+)/routine/view/$', views.RoutineView.as_view(), name='routine-view'),
    url(r'^schedule/routine/edit/(?P<pk>[0-9]+)/$', views.RoutineEdit.as_view(), name='routine-edit'),
    url(r'^schedule/routine/delete/(?P<pk>[0-9]+)/$', views.RoutineDelete.as_view(), name='routine-delete'),

    #create exam routine
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/exam-routine/create/$', views.ExamRoutineCreate.as_view(), name='exam-routine-create'),
    url(r'^schedule/class-list/(?P<classes>[a-zA-Z0-9]+)/exam-routine/view/$', views.ExamRoutineView.as_view(), name='exam-routine-view'),
    url(r'^schedule/class-list/exam-routine/edit/(?P<pk>[0-9]+)/$', views.ExamRoutineEdit.as_view(), name='exam-routine-edit'),
    url(r'^schedule/exam-routine/delete/(?P<pk>[0-9]+)/$', views.ExamRoutineDelete.as_view(), name='exam-routine-delete'),


    #::::end schedule module url::::
    #:::::::::::::::::::::::::::::::::



    #:::::start notice module url:::::
    #:::::::::::::::::::::::::::::::::

    url(r'^notice/$', views.Notice.as_view(), name='notice'),
    url(r'^notice/create/$', views.NoticeCreate.as_view(), name='notice-create'),
    url(r'^notice/class-list/$', views.NoticeClassList.as_view(), name='notice-class-list'),
    url(r'^notice/class-list/(?P<classes>[a-zA-Z0-9]+)/$', views.NoticeList.as_view(), name='notice-list'),
    url(r'^notice/view/(?P<pk>[0-9]+)/$', views.NoticeView.as_view(), name='notice-view'),
    url(r'^notice/edit/(?P<pk>[0-9]+)/$', views.NoticeEdit.as_view(), name='notice-edit'),
    url(r'^notice/delete/(?P<pk>[0-9]+)/$', views.NoticeDelete.as_view(), name='notice-delete'),
    url(r'^notice/search/$', views.NoticeSearch.as_view(), name='notice-search'),

    #::::::end notice module url::::::
    #:::::::::::::::::::::::::::::::::

    #:::::start gallary module url::::
    #:::::::::::::::::::::::::::::::::



    url(r'^gallary/$', views.Gallary.as_view(), name='gallary'),
    url(r'^gallary/image/$', views.GallaryImage.as_view(), name='gallary-image'),
    url(r'^gallary/image/create/$', views.GallaryImageCreate.as_view(), name='gallary-image-create'),
    url(r'^gallary/image/view/$', views.GallaryImageView.as_view(), name='gallary-image-view'),
    url(r'^gallary/image/delete/(?P<pk>[0-9]+)/$', views.GallaryImageDelete.as_view(), name='gallary-image-delete'),


    #::::::end gallary module url::::::
    #:::::::::::::::::::::::::::::::::
]
