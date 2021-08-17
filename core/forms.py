from django import forms
from allauth.account.forms import SignupForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3
from . import models
from metropolis import settings

class MetropolisSignupForm(SignupForm):
    captcha = ReCaptchaField(widget=ReCaptchaV3, label='')
    first_name = forms.CharField(max_length=30, label='First Name', widget=forms.TextInput(attrs={"type": "text", "placeholder": "First Name", "autocomplete": "given-name"}))
    last_name = forms.CharField(max_length=30, label='Last Name', widget=forms.TextInput(attrs={"type": "text", "placeholder": "Last Name", "autocomplete": "family-name"}))
    graduating_year = forms.ChoiceField(choices=models.graduating_year_choices)
    field_order = ['email', 'username', 'first_name', 'last_name', 'graduating_year', 'password1', 'password2', 'captcha']

    def save(self, request):
        user = super(MetropolisSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.graduating_year = self.cleaned_data['graduating_year']
        user.save()
        return user

class AddTimetableSelectTermForm(forms.Form):
    term = forms.ModelChoiceField(queryset=models.Term.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(AddTimetableSelectTermForm, self).__init__(*args, **kwargs)
        self.fields['term'].queryset = models.Term.objects.exclude(timetables__owner=user)

class AddTimetableSelectCoursesForm(forms.ModelForm):
    class Meta:
        model = models.Timetable
        fields = ['courses']
        widgets = {
            'courses': forms.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        self.term = kwargs.pop('term')
        super(AddTimetableSelectCoursesForm, self).__init__(*args, **kwargs)
        self.fields['courses'].queryset = models.Course.objects.filter(term=self.term).order_by('code')

    def clean(self):
        courses = self.cleaned_data['courses']
        if courses.count() > self.term.num_courses:
            raise forms.ValidationError(f'There are only {self.term.num_courses} courses in this term.')
        position_set = set()
        for i in courses:
            if i.position in position_set:
                raise forms.ValidationError(f'There are two or more conflicting courses.')
            else:
                position_set.add(i.position)

class AddCourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['code', 'position']
        widgets = {
            'position': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        self.term = kwargs.pop('term')
        super(AddCourseForm, self).__init__(*args, **kwargs)

        self.fields['position'].label = settings.TIMETABLE_FORMATS[self.term.timetable_format]['question']['prompt']
        self.fields['position'].choices = settings.TIMETABLE_FORMATS[self.term.timetable_format]['question']['choices']

        term_courses = self.term.courses.order_by('?')
        if term_courses:
            self.fields['code'].widget.attrs['placeholder'] = f'Ex. {term_courses[0].code}'

        self.position_set = list(settings.TIMETABLE_FORMATS[self.term.timetable_format]['positions'])
        self.position_set.sort()

    def clean_code(self):
        code = self.cleaned_data['code']
        courses = self.term.courses.filter(code=code)
        if courses:
            raise forms.ValidationError('A course with the same code exists for the selected term.')
        return code

    def clean_position(self):
        position = self.cleaned_data['position']
        if position not in self.position_set:
            raise forms.ValidationError('Must be one of ' + ', '.join([str(i) for i in self.position_set]) + '.')
        return position
