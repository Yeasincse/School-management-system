from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.views import login, logout
from django.views.generic import CreateView

from . import forms
from . import models
from administration.views import AdminPermission


# logout
def logout_request(request):
    logout(request)
    return redirect('account:login')


# registration functionality
class Registration(View):
    """
       How office registration works:
       ------------------------------

       ###if admin user has no school in their user_profile then we consider he has the ability
          to add school and other official.

       ###if admin user has school in their user_profile then we consider he has a school and then
          he can only add official for his school by these view.

    """
    template_name = 'account/registration.html'

    def get(self, request):
        #this variable is to compare user is he has school or not in the template
        current_user_school = request.user.school

        regForm = forms.RegistrationForm()

        variables = {
            'regForm': regForm,
            'current_user_school': current_user_school,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        #this variable is to compare user is he has school or not in the template
        current_user_school = request.user.school

        regForm = forms.RegistrationForm(request.POST or None, request.FILES)

        if regForm.is_valid():
            profile = regForm.registration()
            profile_id = profile.id

            #get available member id from submitting form
            member_type = request.POST.get("member_type")

            #get available member obj for retrive name of the member type for compare
            member_type_obj = models.AvailableUser.objects.filter(id=member_type)

            member_name = False
            for member in member_type_obj:
                member_name = member.name

            #for school
            if member_name == 'school':
                return redirect('account:add-school', pk=profile_id)

        variables = {
            'regForm': regForm,
            'current_user_school': current_user_school,
        }

        return render(request, self.template_name, variables)


class Login(View):
    template_name = 'account/login.html'

    def get(self, request):
        loginForm = forms.LoginForm()

        variables = {
            'loginForm': loginForm,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        loginForm = forms.LoginForm(request.POST or None)

        if loginForm.is_valid():
            user = loginForm.login()
            if user.member_type.id == 4:
                print(user.school)
                print(user.is_authenticated())
                return redirect('student:index')
            if user:
                login(request, user)
                return redirect('administration:home')

        variables = {
            'loginForm': loginForm,
        }

        return render(request, self.template_name, variables)


# registration for teacher
class RegistrationMember(AdminPermission, View):
    template_name = 'account/registration-member.html'

    def get(self, request):
        regForm = forms.RegistrationMemberForm()

        get_school = request.user.school

        variables = {
            'regForm': regForm,
            'get_school': get_school,
        }

        return render(request, self.template_name, variables)

    def post(self, request):
        get_school = request.user.school

        regForm = forms.RegistrationMemberForm(request.POST or None, request.FILES)

        if regForm.is_valid():
            profile = regForm.registration()
            profile_id = profile.id

            # get available member id from submitting form
            member_type = request.POST.get("member_type")

            # get available member obj for retrive name of the member type for compare
            member_type_obj = models.AvailableUser.objects.filter(id=member_type)

            member_name = False
            for member in member_type_obj:
                member_name = member.name

            # for teacher
            if member_name == 'teacher':
                return redirect('account:add-teacher', pk=profile_id)
            # for parent
            elif member_name == 'parent':
                return redirect('account:add-parent', pk=profile_id)
            # for school
            elif member_name == 'school':
                return redirect('account:add-school', pk=profile_id)
            # for student
            elif member_name == 'student':
                return redirect('account:add-student', pk=profile_id)
            # for librarian
            elif member_name == 'librarian':
                return redirect('account:add-librarian', pk=profile_id)

        variables = {
            'regForm': regForm,
            'get_school': get_school,
        }

        return render(request, self.template_name, variables)


# additional information to register teacher
class AddTeacher(AdminPermission, View):
    template_name = 'account/add-teacher.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)
        teacherForm = forms.TeacherForm()

        variables = {
            'teacherForm': teacherForm,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        teacherForm = forms.TeacherForm(request.POST or None)

        if teacherForm.is_valid():
            user = teacherForm.save()
            teacher_id = user.id

            # get teacher object
            teacher_obj = models.Teacher.objects.get(id=teacher_id)

            # update user profile for teacher field
            update_user_profile = models.UserProfile.objects.filter(id=pk).update(teacher=teacher_obj)

            return redirect('administration:add-member')

        variables = {
            'teacherForm': teacherForm,
        }

        return render(request, self.template_name, variables)


# additional information to register teacher
class AddParent(AdminPermission, View):
    template_name = 'account/add-parent.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)
        parentForm = forms.ParentForm()

        variables = {
            'parentForm': parentForm,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        parentForm = forms.ParentForm(request.POST or None)

        if parentForm.is_valid():
            user = parentForm.save()
            parent_id = user.id

            # get parent object
            parent_obj = models.Parent.objects.get(id=parent_id)

            # update user profile for teacher field
            update_user_profile = models.UserProfile.objects.filter(id=pk).update(parent=parent_obj)

            return redirect('administration:add-member')

        variables = {
            'parentForm': parentForm,
        }

        return render(request, self.template_name, variables)


# additional information to register teacher
class AddSchool(AdminPermission, View):
    template_name = 'account/add-school.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)
        schoolForm = forms.SchoolForm()

        variables = {
            'schoolForm': schoolForm,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        schoolForm = forms.SchoolForm(request.POST or None, request.FILES)

        if schoolForm.is_valid():
            user = schoolForm.save()
            school_id = user.id

            # get school object
            school_obj = models.School.objects.get(id=school_id)

            # update user profile for teacher field
            update_user_profile = models.UserProfile.objects.filter(id=pk).update(is_school=True, school=school_obj)

            return redirect('administration:add-member')

        variables = {
            'schoolForm': schoolForm,
        }

        return render(request, self.template_name, variables)


# additional information to register student
class AddStudent(AdminPermission, View):
    template_name = 'account/add-student.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)
        studentForm = forms.StudentForm()

        variables = {
            'studentForm': studentForm,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        studentForm = forms.StudentForm(request.POST or None)

        if studentForm.is_valid():
            user = studentForm.save()
            student_id = user.id

            # get school object
            student_obj = models.Student.objects.get(id=student_id)

            # update user profile for student field
            update_user_profile = models.UserProfile.objects.filter(id=pk).update(student=student_obj)

            return redirect('administration:add-member')

        variables = {
            'studentForm': studentForm,
        }

        return render(request, self.template_name, variables)


# additional information to register librarian
class AddLibrarian(AdminPermission, View):
    template_name = 'account/add-librarian.html'

    def get(self, request, pk):
        get_object_or_404(models.UserProfile, pk=pk)
        librarianForm = forms.LibrarianForm()

        variables = {
            'librarianForm': librarianForm,
        }

        return render(request, self.template_name, variables)

    def post(self, request, pk):
        librarianForm = forms.LibrarianForm(request.POST or None)

        if librarianForm.is_valid():
            user = librarianForm.save()
            librarian_id = user.id

            # get library object
            librarian_obj = models.Librarian.objects.get(id=librarian_id)

            # update user profile for student field
            update_user_profile = models.UserProfile.objects.filter(id=pk).update(librarian=librarian_obj)

            return redirect('administration:add-member')

        variables = {
            'librarianForm': librarianForm,
        }

        return render(request, self.template_name, variables)
