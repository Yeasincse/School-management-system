from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q

from administration.views import AdminPermission

from . import forms
from account import models
from . import models as office_model


def check_user(request, pk):
    user_objects = models.UserProfile.objects.filter(pk=pk)

    user_school_id = False
    for user_obj in user_objects:
        user_school_id = user_obj.school.id

    #compare admin school id to requested user school id for same school retrive
    if user_school_id == request.user.school.id:
        return user_objects


#office home page
class Home(AdminPermission, View):
    template_name = 'office/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#==========================================
#==========================================
#======start member orperation view========
#==========================================
#==========================================

#office registration for other official and student, teacher, parent, librarian
class Registration(AdminPermission, View):
    template_name = 'office/registration.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#member edit view
class MemberSearch(AdminPermission, View):
    template_name = 'office/search.html'

    def get(self, request):
        search_form = forms.SearchForm()

        variables = {
            'search_form': search_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        search_form = forms.SearchForm(request.POST or None)

        queries = None
        count = None
        if search_form.is_valid():
            queries, count = search_form.search(request)

        variables = {
            'search_form': search_form,
            'queries': queries,
            'count': count,
        }

        return render(request, self.template_name, variables)


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


class MemberDelete(AdminPermission, View):
    template_name = 'office/member-delete.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        check_admin_permission = check_user(request, pk)

        viewable_user = False

        if check_admin_permission:
            viewable_user = check_admin_permission

        variables = {
            'viewable_user': viewable_user,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        check_admin_permission = check_user(request, pk)

        viewable_user = False

        if check_admin_permission:
            viewable_user = check_admin_permission

            if request.POST.get('yes') == 'yes':
                member_id = request.POST.get('member_id')

                member_obj = models.UserProfile.objects.get(id=member_id)
                member_obj.delete()

                return redirect('office:member-search')

            elif request.POST.get('no') == 'no':
                member_id = request.POST.get('member_id')
                return redirect('office:member-detail', pk=member_id)

        variables = {
            'viewable_user': viewable_user,
        }

        return render(request, self.template_name, variables)


#office member list
class MemberList(AdminPermission, View):
    template_name = 'office/member-list.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#office member list detail
class MemberListDetail(AdminPermission, View):
    template_name = 'office/member-list-detail.html'

    def get(self, request, type):
        member_type = type

        queries = models.UserProfile.objects.filter(Q(school__id=request.user.school.id) & Q(member_type__name=type)).all()
        count = models.UserProfile.objects.filter(Q(school__id=request.user.school.id) & Q(member_type__name=type)).count()

        variables = {
            'queries': queries,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office class detail
class StudentClass(AdminPermission, View):
    template_name = 'office/student-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school__name=request.user.school.name)).all()
        count = models.Class.objects.filter(Q(school__name=request.user.school.name)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office :: student list in class
class StudenListInClass(AdminPermission, View):
    template_name = 'office/student-list-in-class.html'

    def get(self, request, classes):

        students = models.UserProfile.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes) & Q(member_type__name='student')).all()
        count = models.UserProfile.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes) & Q(member_type__name='student')).count()

        variables = {
            'students': students,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office :: class wise section
class ClassWiseSection(AdminPermission, View):
    template_name = 'office/class-wise-section.html'

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


#office schedule:::class list
class ClassList(AdminPermission, View):
    template_name = 'office/class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school__name=request.user.school.name)).all()
        count = models.Class.objects.filter(Q(school__name=request.user.school.name)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

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
class RoutineCreate(AdminPermission, View):
    template_name = 'office/routine-create.html'

    def get(self, request, classes, section):

        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        class_routine_form = forms.CreateRoutineForm(request=request, classes=classes_obj)

        variables = {
            'class_routine_form': class_routine_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes, section):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        class_routine_form = forms.CreateRoutineForm(request.POST or None, request=request, classes=classes_obj)

        if class_routine_form.is_valid():
            class_routine_form.deploy(section)

        variables = {
            'class_routine_form': class_routine_form,
        }

        return render(request, self.template_name, variables)


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

#routine edit
class RoutineEdit(AdminPermission, View):
    template_name = 'office/routine-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ClassRoutine, pk=pk)



        routine_obj = office_model.ClassRoutine.objects.filter(pk=pk)
        routine_objs = office_model.ClassRoutine.objects.get(pk=pk)

        classes_obj = False
        routine_school = False
        for routines in routine_obj:
            classes_obj = routines.classes
            routine_school = routines.school.name

        routine_edit_form = False
        if routine_school == request.user.school.name:
            routine_edit_form = forms.RoutineEditForm(instance=routine_objs, request=request, classes=classes_obj)

        variables = {
            'routine_edit_form': routine_edit_form,
            'routine_obj': routine_obj,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.ClassRoutine, pk=pk)

        routine_obj = office_model.ClassRoutine.objects.filter(pk=pk)
        routine_objs = office_model.ClassRoutine.objects.get(pk=pk)

        classes_obj = False
        routine_school = False
        for routines in routine_obj:
            classes_obj = routines.classes
            routine_school = routines.school.name

        routine_edit_form = forms.RoutineEditForm(request.POST or None, instance=routine_objs, request=request, classes=classes_obj)

        if routine_school == request.user.school.name:
            if routine_edit_form.is_valid():
                routine_edit_form.save()

        variables = {
            'routine_edit_form': routine_edit_form,
            'routine_obj': routine_obj,
        }

        return render(request, self.template_name, variables)


#routine delete
class RoutineDelete(AdminPermission, View):
    template_name = 'office/routine-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ClassRoutine, pk=pk)

        routine_obj = office_model.ClassRoutine.objects.filter(pk=pk)

        routine_school = False
        for routines in routine_obj:
            routine_school = routines.school.name

        viewable_routine = False
        if routine_school == request.user.school.name:
            viewable_routine = routine_obj

        variables = {
            'viewable_routine': viewable_routine,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)

        routine_obj = office_model.ClassRoutine.objects.filter(pk=pk)

        routine_school = False
        routine_class = False
        routine_section = False
        for routines in routine_obj:
            routine_school = routines.school.name
            routine_class = routines.classes.name
            routine_section = routines.section.name

        viewable_routine = False
        if routine_school == request.user.school.name:
            viewable_routine = routine_obj

            if request.POST.get('yes') == 'yes':
                routine_id = request.POST.get('routine_id')

                routine_obj = office_model.ClassRoutine.objects.get(id=routine_id)
                routine_obj.delete()

                return redirect('office:routine-view', classes=routine_class, section=routine_section)

            elif request.POST.get('no') == 'no':
                return redirect('office:routine-view', classes=routine_class, section=routine_section)

        variables = {
            'viewable_routine': viewable_routine,
        }

        return render(request, self.template_name, variables)


#create exam routine
class ExamRoutineCreate(AdminPermission, View):
    template_name = 'office/exam-routine-create.html'

    def get(self, request, classes):

        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        exam_routine_form = forms.CreateExamRoutineForm(request=request, classes=classes_obj)

        variables = {
            'exam_routine_form': exam_routine_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, classes):
        classes_obj = models.Class.objects.get(Q(school=request.user.school) & Q(name=classes))

        exam_routine_form = forms.CreateExamRoutineForm(request.POST or None, request=request, classes=classes_obj)

        if exam_routine_form.is_valid():
            exam_routine_form.deploy()

        variables = {
            'exam_routine_form': exam_routine_form,
        }

        return render(request, self.template_name, variables)



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


#exam routine edit
class ExamRoutineEdit(AdminPermission, View):
    template_name = 'office/exam-routine-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ExamRoutine, pk=pk)

        routine_obj = office_model.ExamRoutine.objects.filter(pk=pk)
        routine_objs = office_model.ExamRoutine.objects.get(pk=pk)

        classes_obj = False
        routine_school = False
        for routines in routine_obj:
            classes_obj = routines.classes
            routine_school = routines.school.name

        exam_routine_edit_form = False
        if routine_school == request.user.school.name:
            exam_routine_edit_form = forms.ExamRoutineEditForm(instance=routine_objs, request=request, classes=classes_obj)

        variables = {
            'exam_routine_edit_form': exam_routine_edit_form,
            'routine_obj': routine_obj,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.ExamRoutine, pk=pk)

        routine_obj = office_model.ExamRoutine.objects.filter(pk=pk)
        routine_objs = office_model.ExamRoutine.objects.get(pk=pk)

        classes_obj = False
        routine_school = False
        for routines in routine_obj:
            classes_obj = routines.classes
            routine_school = routines.school.name

        exam_routine_edit_form = forms.ExamRoutineEditForm(request.POST or None, instance=routine_objs, request=request, classes=classes_obj)

        if routine_school == request.user.school.name:
            if exam_routine_edit_form.is_valid():
                exam_routine_edit_form.save()

        variables = {
            'exam_routine_edit_form': exam_routine_edit_form,
            'routine_obj': routine_obj,
        }

        return render(request, self.template_name, variables)



#exam routine delete
class ExamRoutineDelete(AdminPermission, View):
    template_name = 'office/exam-routine-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.ExamRoutine, pk=pk)

        routine_obj = office_model.ExamRoutine.objects.filter(pk=pk)

        routine_school = False
        for routines in routine_obj:
            routine_school = routines.school.name

        viewable_routine = False
        if routine_school == request.user.school.name:
            viewable_routine = routine_obj

        variables = {
            'viewable_routine': viewable_routine,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.ExamRoutine, pk=pk)

        routine_obj = office_model.ExamRoutine.objects.filter(pk=pk)

        routine_school = False
        routine_class = False
        for routines in routine_obj:
            routine_school = routines.school.name
            routine_class = routines.classes.name

        viewable_routine = False
        if routine_school == request.user.school.name:
            viewable_routine = routine_obj

            if request.POST.get('yes') == 'yes':
                routine_id = request.POST.get('routine_id')

                routine_obj = office_model.ExamRoutine.objects.get(id=routine_id)
                routine_obj.delete()

                return redirect('office:exam-routine-view', classes=routine_class)

            elif request.POST.get('no') == 'no':
                return redirect('office:exam-routine-view', classes=routine_class)

        variables = {
            'viewable_routine': viewable_routine,
        }

        return render(request, self.template_name, variables)

#==========================================
#==========================================
#======end schedule orperation view========
#==========================================
#==========================================


#==========================================
#==========================================
#======start notice orperation view========
#==========================================
#==========================================


#notice schedule
class Notice(AdminPermission, View):
    template_name = 'office/notice.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#notice create
class NoticeCreate(AdminPermission, View):
    template_name = 'office/notice-create.html'

    def get(self, request):
        create_notice_form = forms.NoticeForm(request=request)

        variables = {
            'create_notice_form': create_notice_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        create_notice_form = forms.NoticeForm(request.POST or None, request=request)

        if create_notice_form.is_valid():
            create_notice_form.deploy(request)

        variables = {
            'create_notice_form': create_notice_form,
        }

        return render(request, self.template_name, variables)


#office notice:::class list
class NoticeClassList(AdminPermission, View):
    template_name = 'office/notice-class-list.html'

    def get(self, request):

        classes = models.Class.objects.filter(Q(school__name=request.user.school.name)).all()
        count = models.Class.objects.filter(Q(school__name=request.user.school.name)).count()

        variables = {
            'classes': classes,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass

#office notice:::notice list
class NoticeList(AdminPermission, View):
    template_name = 'office/notice-list.html'

    def get(self, request, classes):

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).all()
        count = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(classes__name=classes)).count()

        variables = {
            'notices': notices,
            'count': count,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office notice:::notice view
class NoticeView(AdminPermission, View):
    template_name = 'office/notice-view.html'

    def get(self, request, pk):

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk)).all()

        variables = {
            'notices': notices,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass


#office notice:::notice edit
class NoticeEdit(AdminPermission, View):
    template_name = 'office/notice-edit.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Notice, pk=pk)

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        notice_edit_form = forms.NoticeEditForm(request=request, instance=office_model.Notice.objects.get(pk=pk))

        variables = {
            'notices': notices,
            'notice_edit_form': notice_edit_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Notice, pk=pk)

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        notice_edit_form = forms.NoticeEditForm(request.POST or None, request=request, instance=office_model.Notice.objects.get(pk=pk))

        if notice_edit_form.is_valid():
            notice_edit_form.save()

        variables = {
            'notices': notices,
            'notice_edit_form': notice_edit_form,
        }

        return render(request, self.template_name, variables)


#notice delete
class NoticeDelete(AdminPermission, View):
    template_name = 'office/notice-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.Notice, pk=pk)

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_notice = False
        if notices:
            viewable_notice = notices

        variables = {
            'viewable_notice': viewable_notice,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.Notice, pk=pk)

        notices = office_model.Notice.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_notice = False
        if notices:
            viewable_notice = notices

            if request.POST.get('yes') == 'yes':
                routine_id = request.POST.get('notice_id')

                routine_obj = office_model.Notice.objects.get(id=routine_id)
                routine_obj.delete()

                return redirect('office:notice')

            elif request.POST.get('no') == 'no':
                return redirect('office:notice')

        variables = {
            'viewable_notice': viewable_notice,
        }

        return render(request, self.template_name, variables)


#notice search view
class NoticeSearch(AdminPermission, View):
    template_name = 'office/notice-search.html'

    def get(self, request):
        search_form = forms.NoticeSearchForm()

        variables = {
            'search_form': search_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        search_form = forms.NoticeSearchForm(request.POST or None)

        queries = None
        count = None
        if search_form.is_valid():
            queries, count = search_form.search(request)

        variables = {
            'search_form': search_form,
            'queries': queries,
            'count': count,
        }

        return render(request, self.template_name, variables)

#==========================================
#==========================================
#=======end notice orperation view=========
#==========================================
#==========================================


#==========================================
#==========================================
#=====start gallary orperation view========
#==========================================
#==========================================

#gallary
class Gallary(AdminPermission, View):
    template_name = 'office/gallary.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#gallary-image
class GallaryImage(AdminPermission, View):
    template_name = 'office/gallary-image.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        pass


#gallary-image-create
class GallaryImageCreate(AdminPermission, View):
    template_name = 'office/gallary-image-create.html'

    def get(self, request):
        gallary_image_form = forms.GallaryImageForm()

        variables = {
            'gallary_image_form': gallary_image_form,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        gallary_image_form = forms.GallaryImageForm(request.POST or None, request.FILES)

        if gallary_image_form.is_valid():
            gallary_image_form.deploy(request)

        variables = {
            'gallary_image_form': gallary_image_form,
        }

        return render(request, self.template_name, variables)



#gallary-image view
class GallaryImageView(AdminPermission, View):
    template_name = 'office/gallary-image-view.html'

    def get(self, request):

        images = office_model.GallaryImage.objects.filter(school=request.user.school).order_by('-id')

        variables = {
            'images': images,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        pass



#image delete
class GallaryImageDelete(AdminPermission, View):
    template_name = 'office/gallary-image-delete.html'

    def get(self, request, pk):
        get_object_or_404(office_model.GallaryImage, pk=pk)

        images = office_model.GallaryImage.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_image = False
        if images:
            viewable_image = images

        variables = {
            'viewable_image': viewable_image,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        get_object_or_404(office_model.GallaryImage, pk=pk)

        images = office_model.GallaryImage.objects.filter(Q(school__name=request.user.school.name) & Q(pk=pk) & Q(user=request.user))

        viewable_image = False
        if images:
            viewable_image = images

            if request.POST.get('yes') == 'yes':
                image_id = request.POST.get('image_id')

                image_obj = office_model.GallaryImage.objects.get(id=image_id)
                image_obj.delete()

                return redirect('office:gallary-image-view')

            elif request.POST.get('no') == 'no':
                return redirect('office:gallary-image-view')

        variables = {
            'viewable_image': viewable_image,
        }

        return render(request, self.template_name, variables)

#==========================================
#==========================================
#=======end gallary orperation view========
#==========================================
#==========================================
