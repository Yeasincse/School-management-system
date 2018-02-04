from django import forms
from . import models
from django.contrib.auth import authenticate
from django.db.models import Q


import re
from django.utils.timezone import now


# user registration form
class RegistrationForm(forms.Form):
    member_type = forms.ModelChoiceField(models.AvailableUser.objects.filter(Q(name='office') | Q(name='school')), required=False, widget=forms.Select(attrs={'class':'input-field'}))
    school = forms.ModelChoiceField(models.School.objects.all(), required=False, widget=forms.Select(attrs={'class':'input-field'}))
    username = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    email = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'email'}))
    phone = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    address = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )
    account_type = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    password1 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate'}))
    password2 = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password'}))
    photo = forms.ImageField(required=False)


    def clean(self):
        member_type = self.cleaned_data.get('member_type')
        school = self.cleaned_data.get('school')
        username = self.cleaned_data.get('username')
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        address = self.cleaned_data.get('address')
        account_type = self.cleaned_data.get('account_type')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        photo = self.cleaned_data.get('photo')

        if len(username) < 1:
            raise forms.ValidationError("Enter username!")
        else:
            user_exist = models.UserProfile.objects.filter(username__iexact=username).exists()
            if user_exist:
                raise forms.ValidationError("Username already taken!")
            else:
                if len(email) < 1:
                    raise forms.ValidationError("Enter email address!")
                else:
                    email_correction = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
                    if email_correction == None:
                        raise forms.ValidationError("Email not correct!")
                    else:
                        email_exist = models.UserProfile.objects.filter(email__iexact=email).exists()
                        if email_exist:
                            raise forms.ValidationError("Email already exist!")
                        else:
                            if len(password1) < 8:
                                raise forms.ValidationError("Password is too short!")
                            else:
                                if password1 != password2:
                                    raise forms.ValidationError("Password not matched!")

    def registration(self):
        member_type = self.cleaned_data.get('member_type')
        school = self.cleaned_data.get('school')
        username = self.cleaned_data.get('username')
        name = self.cleaned_data.get('name')
        email = self.cleaned_data.get('email')
        phone = self.cleaned_data.get('phone')
        address = self.cleaned_data.get('address')
        account_type = self.cleaned_data.get('account_type')
        password1 = self.cleaned_data.get('password1')
        photo = self.cleaned_data.get('photo')

        user = models.UserProfile.objects.create_user(username=username, email=email, name=name, phone=phone, address=address, school=school, photo=photo)
        user.set_password(password1)

        # if official set account type 'admin' or 'superuser'
        if account_type == 'admin' or account_type == 'superuser':
            user.is_staff = True
            user.is_superuser = True
        else:
            pass

        user.member_type = member_type
        user.account_type = account_type
        user.last_login = now()

        user.save()
        return user


# login form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'validate', 'id': 'icon_prefix',}))
    password = forms.CharField(max_length=20, required=False, widget=forms.PasswordInput(attrs={'class': 'validate', 'id': 'password'}))

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if len(username) < 1:
            raise forms.ValidationError("Enter Username!")
        else:
            if len(password) < 8:
                raise forms.ValidationError("Password is too short!")
            else:
                user = authenticate(username=username, password=password)
                if not user or not user.is_active:
                    raise forms.ValidationError("Username or Password not matched!")
        return self.cleaned_data

    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


# Member registration
class RegistrationMemberForm(RegistrationForm):
    member_type = forms.ModelChoiceField(models.AvailableUser.objects.all().exclude(Q(pk=1) | Q(pk=4)), required=False, widget=forms.Select(attrs={'class':'input-field'}))

# add teacher form
gender_list = (
        ('male', 'Male'),
        ('female', 'Female'),)

class TeacherForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=gender_list, required=False, widget=forms.Select(attrs={'class': 'validate'}))
    class Meta:
        model = models.Teacher
        fields = '__all__'

    def clean(self):
        position = self.cleaned_data.get('position')
        salary = self.cleaned_data.get('salary')
        gender = self.cleaned_data.get('gender')

        if not position:
            raise forms.ValidationError("Enter teacher Position!")
        else:
            if not salary:
                raise forms.ValidationError("Enter Teacher Salary!")
            if not gender:
                raise forms.ValidationError("Select Gender!")


# add parent form
class ParentForm(forms.ModelForm):
    class Meta:
        model = models.Parent
        fields = '__all__'


# add school form
class SchoolForm(forms.ModelForm):
    address = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )

    class Meta:
        model = models.School
        fields = '__all__'


    def clean(self):
        name = self.cleaned_data.get('name')
        description = self.cleaned_data.get('description')
        logo = self.cleaned_data.get('logo')
        banner = self.cleaned_data.get('banner')
        address = self.cleaned_data.get('address')
        website = self.cleaned_data.get('website')
        phone = self.cleaned_data.get('phone')

        if not name:
            raise forms.ValidationError('Enter School name!')
        else:
            if not address:
                raise forms.ValidationError('Enter School Address!')
            else:
                if not phone:
                    raise forms.ValidationError('Enter Phone number!')

# add student form
class StudentForm(forms.ModelForm):
    birthday = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    gender = forms.ChoiceField(choices=gender_list, required=False, widget=forms.Select(attrs={'class': 'validate'}))

    class Meta:
        model = models.Student
        fields = '__all__'

    def clean(self):
        roll = self.cleaned_data.get('roll')
        birthday = self.cleaned_data.get('birthday')
        gender = self.cleaned_data.get('gender')
        school_bus = self.cleaned_data.get('school_bus')

        if not roll:
            raise forms.ValidationError('Enter Roll!')
        else:
            if not birthday:
                raise forms.ValidationError('Enter Birthday!')
            else:
                if not gender:
                    raise forms.ValidationError('Select Gender!')
                else:
                    if not school_bus:
                        raise forms.ValidationError('Enter School Bus!')


# add librarian form
class LibrarianForm(forms.ModelForm):
    birthday = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    gender = forms.ChoiceField(choices=gender_list, required=False, widget=forms.Select(attrs={'class': 'validate'}))

    class Meta:
        model = models.Librarian
        fields = '__all__'

    def clean(self):
        birthday = self.cleaned_data.get('birthday')
        gender = self.cleaned_data.get('gender')

        if not birthday:
            raise forms.ValidationError('Enter Birthday!')
        else:
            if not gender:
                raise forms.ValidationError('Select Gender!')
