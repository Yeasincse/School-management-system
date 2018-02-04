from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q

from administration.views import AdminPermission

#from . import forms
from account import models
from account.views import *
from . import models as office_model


def check_user(request, pk):
    user_objects = models.UserProfile.objects.filter(pk=pk)

    user_school_id = False
    for user_obj in user_objects:
        user_school_id = user_obj.school.id

    #compare admin school id to requested user school id for same school retrive
    if user_school_id == request.user.school.id:
        return user_objects


#student home page
def studenthome(request):
    return render(request,'student/index.html')

#==========================================
#==========================================
#======start member orperation view========
#==========================================
#==========================================


#member detail view
class MemberDetail(AdminPermission, View):
    template_name = 'office/member-detail.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        #requested user object
        user_objects = models.UserProfile.objects.filter(pk=pk)

        user_school_id = None
        viewable_user = None

        for user_obj in user_objects:
            user_school_id = user_obj.school.id

        #compare admin school id to requested user school id for same school retrive
        if user_school_id == request.user.school.id:
            viewable_user = user_objects

        variables = {
            'viewable_user': viewable_user,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        pass


class MemberEdit(AdminPermission, View):
    template_name = 'office/member-edit.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        member_edit_form = forms.MemberEditForm(instance=models.UserProfile.objects.get(pk=pk), request=request)

        check_admin_permission = check_user(request, pk)

        viewable_user = False

        if check_admin_permission:
            viewable_user = check_admin_permission

        variables = {
            'viewable_user': viewable_user,
            'member_edit_form': member_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        member_edit_form = forms.MemberEditForm(request.POST or None, request.FILES, instance=models.UserProfile.objects.get(pk=pk), request=request)

        check_admin_permission = check_user(request, pk)

        viewable_user = False

        if check_admin_permission:
            viewable_user = check_admin_permission

            if member_edit_form.is_valid():
                member_edit_form.save()

        variables = {
            'viewable_user': viewable_user,
            'member_edit_form': member_edit_form,
        }

        return render(request, self.template_name, variables)


#office member list
class MemberList(AdminPermission, View):
    template_name = 'office/member-list.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass






#office :: section wise student
class SectionWiseStudent(AdminPermission, View):
    template_name = 'office/section-wise-student.html'

    def get(self, request, classes, section):

        students = models.UserProfile.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes) & Q(section__name=section) & Q(member_type__name='student')).all()
        count = models.UserProfile.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes) & Q(section__name=section) & Q(member_type__name='student')).count()

        variables = {
            'students': students,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass

#==========================================
#==========================================
#=======end member orperation view=========
#==========================================
#==========================================



#==========================================
#==========================================
#=====start schedule orperation view=======
#==========================================
#==========================================


#office schedule
class Schedule(AdminPermission, View):
    template_name = 'office/schedule.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass




#office schedule:::section list
class SectionList(AdminPermission, View):
    template_name = 'office/section-list.html'

    def get(self, request, classes):

        sections = models.Section.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).all()
        count = models.Section.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).count()

        variables = {
            'sections': sections,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office schedule::::routine create


#routine view
class RoutineView(AdminPermission, View):
    template_name = 'office/routine-view.html'

    def get(self, request, classes, section):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))
        section_obj = models.Section.objects.get(Q(school=request.user.school) & Q(classes=classes_obj) & Q(name=section))

        routines = office_model.ClassRoutine.objects.filter(Q(school=request.user.school) & Q(classes=classes_obj) & Q(section=section_obj)).all()

        variables = {
            'routines': routines,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#exam routine view
class ExamRoutineView(AdminPermission, View):
    template_name = 'office/exam-routine-view.html'

    def get(self, request, classes):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        routines = office_model.ExamRoutine.objects.filter(Q(school=request.user.school) & Q(classes=classes_obj)).all()

        variables = {
            'routines': routines,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass




#==========================================
#==========================================
#======end schedule orperation view========
#==========================================
#==========================================
