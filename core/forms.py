from allauth.account.forms import SignupForm
from django import forms
from django.conf import settings
from django.contrib.auth.forms import (
    AdminUserCreationForm as ContribAdminUserCreationForm,
)
from django.contrib.auth.forms import UserChangeForm as ContribUserChangeForm
from django_select2 import forms as s2forms
from martor.widgets import AdminMartorWidget

from core import models
from core.views.mixins import CaseInsensitiveUsernameMixin


class MetropolisSignupForm(SignupForm, CaseInsensitiveUsernameMixin):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        widget=forms.TextInput(attrs={"type": "text", "autocomplete": "given-name"}),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        widget=forms.TextInput(attrs={"type": "text", "autocomplete": "family-name"}),
    )
    graduating_year = forms.ChoiceField(
        choices=models.graduating_year_choices, required=False
    )
    field_order = [
        "email",
        "username",
        "first_name",
        "last_name",
        "graduating_year",
        "password1",
        "password2",
    ]

    def save(self, request):
        user = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.graduating_year = self.cleaned_data["graduating_year"]
        if self.cleaned_data["email"].endswith(settings.TEACHER_EMAIL_SUFFIX):
            user.is_teacher = True
        user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields["email"].widget.attrs["placeholder"]
        del self.fields["username"].widget.attrs["placeholder"]
        del self.fields["password1"].widget.attrs["placeholder"]
        del self.fields["password2"].widget.attrs["placeholder"]

    def clean_email(self):
        email = super().clean_email()
        if not (
            email.endswith(settings.STUDENT_EMAIL_SUFFIX)
            or email.endswith(settings.TEACHER_EMAIL_SUFFIX)
        ):
            raise forms.ValidationError("A TDSB email must be used.")
        return email

    def clean_graduating_year(self):
        graduating_year = self.cleaned_data["graduating_year"]
        if graduating_year == "":
            return None
        return graduating_year


class CourseForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        def filled(field):
            return field in self.cleaned_data and self.cleaned_data[field]

        if not filled("name") and (filled("room") or filled("teacher")):
            raise forms.ValidationError(
                "A course must have a name if it has a room or teacher."
            )

        return cleaned_data

    def is_empty(self):
        return not any(
            self.cleaned_data.get(field) for field in ["name", "room", "teacher"]
        )

    class Meta:
        model = models.Course
        fields = ["name", "room", "teacher"]
        labels = {
            "name": "Course",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Course name or code"}
            ),
            "room": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "(optional)"}
            ),
            "teacher": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "(optional)"}
            ),
        }


CourseFormSet = forms.inlineformset_factory(
    models.Timetable,
    models.Course,
    form=CourseForm,
    extra=0,
    can_delete=False,
)


class TimetableCreateOrUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Timetable
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "autofocus": True,
                    "placeholder": "Title",
                }
            ),
        }


class SelectCoursesWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "code__icontains",
    ]


class OrganizationAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            "extra_content": AdminMartorWidget,
        }

    # TODO: refactor and/or move to org m2m_changed signal
    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk is None:
            owners = cleaned_data.get("owners")
        else:
            owners = cleaned_data.get("owners") or self.instance.owners.all()
        execs = cleaned_data.get("execs")

        if owners is None:
            return

        for owner in owners:
            if execs is not None and owner not in execs:
                raise forms.ValidationError(
                    {"execs": "The owner must also be an exec."}
                )


class EventAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: settings.TIMETABLE_FORMAT or whatever is gone now,
        #       so switch to some other reliable method
        # self.fields["is_instructional"].disabled = True


class TagSuperuserAdminForm(forms.ModelForm):
    class Meta:
        model = models.Tag
        fields = "__all__"


class TagAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_organization(self):
        if self.cleaned_data["organization"] is None:
            raise forms.ValidationError("Tags must have an organization.")
        return self.cleaned_data["organization"]

    class Meta:
        model = models.Tag
        fields = "__all__"


class DailyAnnouncementAdminForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date is not None and end_date is not None and start_date > end_date:
            raise forms.ValidationError(
                {"start_date": "Start date cannot be after end date"}
            )


class AnnouncementAdminForm(forms.ModelForm):
    status = forms.ChoiceField(
        widget=forms.Select(),
        choices=models.announcement_status_initial_choices,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "status" in self.fields:
            self.fields["status"].initial = "d"


class AnnouncementSupervisorAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "status" in self.fields:
            self.fields["status"].initial = "d"


class UserAdminForm(CaseInsensitiveUsernameMixin, ContribUserChangeForm):
    expo_notif_tokens = forms.JSONField(required=False)


class UserCreationAdminForm(CaseInsensitiveUsernameMixin, ContribAdminUserCreationForm):
    pass
