from django import forms
from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from . import models

class CourseShareSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')
    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(attrs={"type": "text", "placeholder": "First Name", "autocomplete": "given-name"}))
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(attrs={"type": "text", "placeholder": "Last Name", "autocomplete": "family-name"}))
    school = forms.ModelChoiceField(queryset=models.School.objects.all())
    field_order = ['email', 'username', 'first_name', 'last_name', 'school', 'password1', 'password2', 'captcha']

    def save(self, request):
        user = super(CourseShareSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        print(self.cleaned_data['school'])
        user.school = self.cleaned_data['school']
        user.save()
        return user

class AddTimetableForm(forms.ModelForm):
    class Meta:
        model = models.Timetable
        fields = ['term', 'courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddTimetableForm, self).__init__(*args, **kwargs)
        self.fields['term'].queryset = models.Term.objects.exclude(timetables__owner=user)

    def clean(self):
        courses = self.cleaned_data['courses']
        term = self.cleaned_data['term']
        if courses.count() > term.num_courses:
            raise forms.ValidationError(f'There are only {term.num_courses} courses in this term.')
        position_set = set()
        for i in courses:
            if i.position in position_set:
                raise forms.ValidationError(f'There are two or more conflicting courses.')
            else:
                position_set.add(i.position)
