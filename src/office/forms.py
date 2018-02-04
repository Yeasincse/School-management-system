from django import forms
from django.db.models import Q

import re

from account import models
from .models import ClassRoutine, ExamRoutine, Notice, GallaryImage


#search form
class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    def clean(self):
        search_text = self.cleaned_data.get('search_text')

    def identify_username_or_email(self, search_text):
        is_email = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', search_text)

        if is_email:
            type = 'email'
        else:
            type = 'username'

        return type


    def search(self, request):
        search_text = self.cleaned_data.get('search_text')

        #admin school id for search in same school
        admin_school_id = request.user.school.id

        check_email_or_username = self.identify_username_or_email(search_text)

        count = None
        query = None
        if check_email_or_username == 'email':
            count = models.UserProfile.objects.filter(Q(email__contains=search_text) & Q(school__id=admin_school_id)).count()
            query = models.UserProfile.objects.filter(Q(email__contains=search_text) & Q(school__id=admin_school_id)).all()
        elif check_email_or_username == 'username':
            count = models.UserProfile.objects.filter(Q(username__contains=search_text) & Q(school__id=admin_school_id)).count()
            query = models.UserProfile.objects.filter(Q(username__contains=search_text) & Q(school__id=admin_school_id)).all()

        return query, count


#member edit form
class MemberEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(MemberEditForm, self).__init__(*args,**kwargs)
        self.fields['classes'].queryset = models.Class.objects.filter(school=self.request.user.school)
        self.fields['section'].queryset = models.Section.objects.filter(school=self.request.user.school)
        self.fields['school'].queryset = models.School.objects.filter(id=self.request.user.school.id)

    address = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )
    classes = forms.ModelChoiceField(queryset=models.Class.objects.all(), required=False, widget=forms.Select(attrs={'class':'input-field browser-default'}))
    section = forms.ModelChoiceField(queryset=models.Section.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    school = forms.ModelChoiceField(queryset=models.School.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))

    class Meta:
        model = models.UserProfile
        fields = ('username', 'name', 'email', 'phone', 'address', 'photo', 'school', 'classes', 'section')




#create routine form
day_list = (
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('saturday', 'Saturday'),)

class CreateRoutineForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        super(CreateRoutineForm, self).__init__(*args,**kwargs)

        self.fields['subject'].queryset = models.Subject.objects.filter(Q(school=self.request.user.school) & Q(classes=self.classes))


    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    day = forms.ChoiceField(choices=day_list, required=False, widget=forms.Select(attrs={'class': 'validate browser-default'}))
    period = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    start_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))
    end_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    def clean(self):
        subject = self.cleaned_data.get('subject')
        day = self.cleaned_data.get('day')
        period = self.cleaned_data.get('period')
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')

        if subject == None:
            raise forms.ValidationError("Select Subject!")
        else:
            if len(start_hour) < 1:
                raise forms.ValidationError('Select Class Start Hour!')
            else:
                if len(end_hour) < 1:
                    raise forms.ValidationError("Select Class End Hour!")


    def deploy(self, section):
        subject = self.cleaned_data.get('subject')
        day = self.cleaned_data.get('day')
        period = self.cleaned_data.get('period')
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')

        section_obj = models.Section.objects.get(Q(school=self.request.user.school) & Q(classes=self.classes) & Q(name=section))

        deploy = ClassRoutine(school=self.request.user.school, classes=self.classes, section=section_obj, subject=subject, day=day, period=period, start_hour=start_hour, end_hour=end_hour)
        deploy.save()


#routine edit form
class RoutineEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        super(RoutineEditForm, self).__init__(*args,**kwargs)

        self.fields['subject'].queryset = models.Subject.objects.filter(Q(school=self.request.user.school) & Q(classes=self.classes))

    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    day = forms.ChoiceField(choices=day_list, required=False, widget=forms.Select(attrs={'class': 'validate browser-default'}))
    period = forms.IntegerField(required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    start_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))
    end_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    class Meta:
        model = ClassRoutine
        fields = ('subject', 'day', 'period', 'start_hour', 'end_hour',)


#exam routine create
class CreateExamRoutineForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        super(CreateExamRoutineForm, self).__init__(*args,**kwargs)

        self.fields['subject'].queryset = models.Subject.objects.filter(Q(school=self.request.user.school) & Q(classes=self.classes))


    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    exam_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    start_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))
    end_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    def clean(self):
        subject = self.cleaned_data.get('subject')
        exam_name = self.cleaned_data.get('exam_name')
        date = self.cleaned_data.get('date')
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')

        if subject == None:
            raise forms.ValidationError("Select Subject!")
        else:
            if exam_name == None:
                raise forms.ValidationError('Enter Exam Name!')
            else:
                if date == None:
                    raise forms.ValidationError('Select exam date!')
                else:
                    if len(start_hour) < 1:
                        raise forms.ValidationError('Select Exam Start Hour!')
                    else:
                        if len(end_hour) < 1:
                            raise forms.ValidationError("Select Exam End Hour!")


    def deploy(self):
        subject = self.cleaned_data.get('subject')
        exam_name = self.cleaned_data.get('exam_name')
        date = self.cleaned_data.get('date')
        start_hour = self.cleaned_data.get('start_hour')
        end_hour = self.cleaned_data.get('end_hour')

        deploy = ExamRoutine(school=self.request.user.school, classes=self.classes, subject=subject, exam_name=exam_name, date=date, start_hour=start_hour, end_hour=end_hour)
        deploy.save()


#exam routine edit form
class ExamRoutineEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        self.classes = kwargs.pop('classes')
        super(ExamRoutineEditForm, self).__init__(*args,**kwargs)

        self.fields['subject'].queryset = models.Subject.objects.filter(Q(school=self.request.user.school) & Q(classes=self.classes))

    subject = forms.ModelChoiceField(queryset=models.Subject.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    exam_name = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    date = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate datepicker'}))
    start_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))
    end_hour = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate timepicker'}))

    class Meta:
        model = ClassRoutine
        fields = ('subject', 'exam_name', 'date', 'start_hour', 'end_hour',)


#create notice
class NoticeForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(NoticeForm, self).__init__(*args,**kwargs)

        self.fields['classes'].queryset = models.Class.objects.filter(Q(school=self.request.user.school))


    classes = forms.ModelChoiceField(queryset=models.Class.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )


    def clean(self):
        classes = self.cleaned_data.get('classes')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')

        if classes == None:
            raise forms.ValidationError('Select Class!')
        else:
            if len(title) == 0:
                raise forms.ValidationError('Write Title!')
            else:
                if len(description) == 0:
                    raise forms.ValidationError('Write description!')

    def deploy(self, request):
        classes = self.cleaned_data.get('classes')
        title = self.cleaned_data.get('title')
        description = self.cleaned_data.get('description')

        deploy = Notice(school=request.user.school, classes=classes, user=request.user, title=title, description=description)
        deploy.save()



#edit notice
class NoticeEditForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        self.request = kwargs.pop('request')
        super(NoticeEditForm, self).__init__(*args,**kwargs)

        self.fields['classes'].queryset = models.Class.objects.filter(Q(school=self.request.user.school))


    classes = forms.ModelChoiceField(queryset=models.Class.objects.all(), required=False,widget=forms.Select(attrs={'class':'input-field browser-default'}))
    title = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))
    description = forms.CharField( required=False, max_length= 1000 ,widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}) )


    class Meta:
        model = Notice
        fields = ('classes', 'title', 'description')



# notice search form
class NoticeSearchForm(forms.Form):
    search_text = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'validate'}))

    def clean(self):
        search_text = self.cleaned_data.get('search_text')

    def search(self, request):
        search_text = self.cleaned_data.get('search_text')

        count = Notice.objects.filter(Q(id=search_text) & Q(school=request.user.school)).count()
        query = Notice.objects.filter(Q(id=search_text) & Q(school=request.user.school)).all()

        return query, count


#gallary image upload form
class GallaryImageForm(forms.Form):
    description = forms.CharField(required=False, max_length=1000, widget=forms.Textarea(attrs={'class': 'validate materialize-textarea'}))
    image = forms.ImageField(required=False)


    def clean(self):
        description = self.cleaned_data.get('description')
        image = self.cleaned_data.get('image')

        if len(description) == 0:
            raise forms.ValidationError('Write Description for this photo!')
        else:
            if image == None:
                raise forms.ValidationError('Choose Image!')


    def deploy(self, request):
        description = self.cleaned_data.get('description')
        image = self.cleaned_data.get('image')

        deploy = GallaryImage(school=request.user.school, user=request.user, description=description, image=image)

        deploy.save()
