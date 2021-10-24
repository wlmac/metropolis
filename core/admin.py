import django.db
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.db.models import Q
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from martor.widgets import AdminMartorWidget

from core.utils.mail import send_mail
from metropolis import settings

from . import models
from .forms import (
    EventAdminForm,
    OrganizationAdminForm,
    TagAdminForm,
    TagSuperuserAdminForm,
    TermAdminForm,
)

User = get_user_model()


# Register your models here.


class CourseInline(admin.TabularInline):
    formfield_overrides = {
        django.db.models.TextField: {"widget": forms.Textarea(attrs={"rows": 1})},
    }
    fields = ["code", "position", "description"]
    ordering = ["code"]
    model = models.Course
    extra = 0


class TermAdmin(admin.ModelAdmin):
    inlines = [
        CourseInline,
    ]
    list_display = ["name", "timetable_format", "start_date", "end_date"]
    form = TermAdminForm


class TagAdmin(admin.ModelAdmin):
    form = TagAdminForm
    readonly_fields = ["color"]
    list_display = ["name", "organization", "color"]
    search_fields = ["name"]

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            return TagSuperuserAdminForm
        return TagAdminForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization__execs=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization":
            if not request.user.is_superuser:
                kwargs["queryset"] = models.Organization.objects.filter(
                    execs=request.user
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class TagInline(admin.StackedInline):
    formfield_overrides = {
        django.db.models.TextField: {"widget": forms.Textarea(attrs={"rows": 1})},
    }
    model = models.Tag
    extra = 0


class OrganizationURLInline(admin.StackedInline):
    fields = ["url"]
    model = models.OrganizationURL
    extra = 0


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "show_members", "is_open", "owner"]
    list_filter = ["is_open", "show_members", "tags"]
    fields = [
        "name",
        "bio",
        "extra_content",
        "slug",
        "show_members",
        "is_open",
        "applications_open",
        "tags",
        "owner",
        "supervisors",
        "execs",
        "banner",
        "icon",
    ]
    autocomplete_fields = ["owner", "execs"]
    search_fields = ["name"]
    inlines = [
        TagInline,
        OrganizationURLInline,
    ]
    form = OrganizationAdminForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(owner=request.user) | Q(execs=request.user)).distinct()

    def get_readonly_fields(self, request, obj=None):
        if obj == None or request.user.is_superuser or request.user == obj.owner:
            return []
        else:
            return ["owner", "supervisors", "execs"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "supervisors":
            kwargs["queryset"] = models.User.objects.filter(is_teacher=True).order_by(
                "username"
            )
        if db_field.name == "execs":
            kwargs["queryset"] = models.User.objects.all().order_by("username")
        if db_field.name == "tags":
            kwargs["queryset"] = models.Tag.objects.filter(
                Q(organization=None) | Q(organization__execs=request.user)
            ).distinct()
            if request.user.is_superuser:
                kwargs["queryset"] = models.Tag.objects.all()
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class OrganizationListFilter(admin.SimpleListFilter):
    title = "organization"
    parameter_name = "org"

    def lookups(self, request, model_admin):
        qs = models.Organization.objects.all()
        if not request.user.is_superuser:
            qs = qs.filter(
                Q(owner=request.user)
                | Q(supervisors=request.user)
                | Q(execs=request.user)
            ).distinct()
        for org in qs:
            yield (org.slug, org.name)

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset
        else:
            return queryset.filter(organization__slug=self.value())


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["__str__", "organization", "status"]
    list_filter = [OrganizationListFilter, "status"]
    ordering = ["-created_date"]
    empty_value_display = "Not specified."
    formfield_overrides = {
        django.db.models.TextField: {"widget": AdminMartorWidget},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(
            Q(organization__supervisors=request.user)
            | Q(organization__execs=request.user)
        ).distinct()

    def get_readonly_fields(self, request, obj=None):
        if obj == None or request.user.is_superuser:
            return []

        all_fields = [
            "organization",
            "author",
            "title",
            "body",
            "tags",
            "is_public",
            "status",
            "rejection_reason",
            "supervisor",
        ]
        status_idx = ["p", "a", "r"].index(obj.status)

        fields = set(all_fields)
        fields_matrix = [
            [
                {"author", "organization", "title", "tags", "is_public"},
                {
                    "author",
                    "organization",
                    "title",
                    "body",
                    "tags",
                    "is_public",
                    "status",
                    "supervisor",
                },
                {
                    "author",
                    "organization",
                    "title",
                    "body",
                    "tags",
                    "is_public",
                    "status",
                    "rejection_reason",
                    "supervisor",
                },
            ],
            [
                {"author", "organization", "status"},
                {"author", "organization", "status", "supervisor"},
                {"author", "organization", "status", "supervisor", "rejection_reason"},
            ],
        ]

        if request.user in obj.organization.supervisors.all():
            fields.intersection_update(fields_matrix[0][status_idx])
        if request.user in obj.organization.execs.all():
            fields.intersection_update(fields_matrix[1][status_idx])

        fields = list(fields)
        fields.sort(key=lambda x: all_fields.index(x))

        return fields

    def get_fields(self, request, obj=None):
        all_fields = [
            "organization",
            "author",
            "title",
            "body",
            "tags",
            "is_public",
            "status",
            "rejection_reason",
            "supervisor",
        ]

        fields = set(all_fields)
        fields.difference_update(self.get_exclude(request, obj))

        fields = list(fields)
        fields.sort(key=lambda x: all_fields.index(x))

        return fields

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return {}

        if obj == None:
            return {"author", "supervisor", "status", "rejection_reason"}

        status_idx = ["p", "a", "r"].index(obj.status)

        fields = {
            "title",
            "body",
            "tags",
            "organization",
            "is_public",
            "supervisor",
            "status",
            "rejection_reason",
        }
        fields_matrix = [
            [{"supervisor"}, {"rejection_reason"}, {}],
            [{"supervisor", "rejection_reason"}, {"rejection_reason"}, {}],
        ]

        if request.user in obj.organization.supervisors.all():
            fields.intersection_update(fields_matrix[0][status_idx])
        if request.user in obj.organization.execs.all():
            fields.intersection_update(fields_matrix[1][status_idx])

        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization":
            if request.user.is_superuser:
                kwargs["queryset"] = models.Organization.objects.all().order_by("name")
            else:
                kwargs["queryset"] = (
                    models.Organization.objects.filter(
                        Q(supervisors=request.user) | Q(execs=request.user)
                    )
                    .distinct()
                    .order_by("name")
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = (
                models.Tag.objects.filter(
                    Q(organization=None) | Q(organization__execs=request.user)
                )
                .distinct()
                .order_by("name")
            )
            if request.user.is_superuser:
                kwargs["queryset"] = models.Tag.objects.all().order_by("name")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if (
            obj != None
            and obj.status != "p"
            and not request.user.is_superuser
            and request.user in obj.organization.supervisors.all()
            and request.user not in obj.organization.execs.all()
        ):
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        if not request.user.is_superuser:
            if request.user in obj.organization.supervisors.all():
                obj.supervisor = request.user
                if obj.status != "p" and request.user != obj.author:
                    # Notify user
                    pass
                    self.message_user(
                        request,
                        f"Successfully marked announcement as {obj.get_status_display()}.",
                    )
            else:
                if (not change) or obj.status != "p":
                    # Notify supervisors

                    for teacher in obj.organization.supervisors.all():
                        email_template_context = {
                            "teacher": teacher,
                            "announcement": obj,
                            "review_link": settings.SITE_URL
                            + reverse("admin:core_announcement_change", args=(obj.pk,)),
                        }

                        send_mail(
                            f"[ACTION REQUIRED] An announcement for {obj.organization.name} needs your approval.",
                            render_to_string(
                                "core/email/verify_announcement.txt",
                                email_template_context,
                            ),
                            None,
                            [teacher.email],
                            bcc=settings.ANNOUNCEMENT_APPROVAL_BCC_LIST,
                            html_message=render_to_string(
                                "core/email/verify_announcement.html",
                                email_template_context,
                            ),
                        )

                    self.message_user(
                        request, f"Successfully sent announcement for review."
                    )
                obj.status = "p"

        super().save_model(request, obj, form, change)


class BlogPostAuthorListFilter(admin.SimpleListFilter):
    title = "author"
    parameter_name = "author"

    def lookups(self, request, model_admin):
        qs = User.objects.filter(blogposts_authored__isnull=False).distinct()
        for author in qs:
            yield (author.pk, author.username)

    def queryset(self, request, queryset):
        if self.value() == None:
            return queryset
        else:
            return queryset.filter(author__pk=self.value())


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "is_published"]
    list_filter = [BlogPostAuthorListFilter, "is_published"]
    ordering = ["-created_date"]
    fields = [
        "author",
        "title",
        "slug",
        "body",
        "featured_image",
        "tags",
        "is_published",
    ]
    formfield_overrides = {
        django.db.models.TextField: {"widget": AdminMartorWidget},
    }

    def get_changeform_initial_data(self, request):
        return {"author": request.user.pk}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = (
                models.Tag.objects.filter(
                    Q(organization=None) | Q(organization__execs=request.user)
                )
                .distinct()
                .order_by("name")
            )
            if request.user.is_superuser:
                kwargs["queryset"] = models.Tag.objects.all().order_by("name")
        return super().formfield_for_manytomany(db_field, request, **kwargs)


class EventAdmin(admin.ModelAdmin):
    list_display = ["name", "organization", "start_date", "end_date"]
    list_filter = [OrganizationListFilter]
    ordering = ["-start_date", "-end_date"]
    search_fields = ["name"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(organization__execs=request.user)

    def get_exclude(self, request, obj=None):
        if not request.user.is_superuser:
            return {"schedule_format", "is_instructional"}

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs["form"] = EventAdminForm
        return super().get_form(request, obj, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = (
                models.Tag.objects.filter(
                    Q(organization=None) | Q(organization__execs=request.user)
                )
                .distinct()
                .order_by("name")
            )
            if request.user.is_superuser:
                kwargs["queryset"] = models.Tag.objects.all().order_by("name")
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization":
            if not request.user.is_superuser:
                kwargs["queryset"] = models.Organization.objects.filter(
                    execs=request.user
                ).order_by("name")
            if request.user.is_superuser:
                kwargs["queryset"] = models.Organization.objects.all().order_by("name")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if (
            obj != None
            and (not request.user.is_superuser)
            and (request.user not in obj.organization.execs.all())
        ):
            return False
        return super().has_change_permission(request, obj)


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "is_superuser", "is_staff", "is_teacher"]
    list_filter = [
        "is_superuser",
        "is_staff",
        "is_teacher",
        "groups",
        "graduating_year",
    ]
    search_fields = ["username", "first_name", "last_name"]

    def has_view_permission(self, request, obj=None):
        if obj == None and (
            request.user.organizations_owning.exists()
            or request.user.organizations_leading.exists()
        ):
            return True

        return super().has_view_permission(request, obj)

    def has_module_permission(self, request):
        return request.user.has_perm("core.view_user") or request.user.is_superuser


class TimetableAdmin(admin.ModelAdmin):
    list_display = ["__str__", "term"]
    list_filter = ["term"]


class FlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        django.db.models.TextField: {"widget": AdminMartorWidget},
    }
    fieldsets = (
        (None, {"fields": ("url", "title", "content", "sites")}),
        (
            _("Advanced options"),
            {
                "classes": ("collapse",),
                "fields": (
                    "registration_required",
                    "template_name",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
admin.site.register(models.Timetable, TimetableAdmin)
admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.Announcement, AnnouncementAdmin)
admin.site.register(models.BlogPost, BlogPostAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Event, EventAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)

admin.site.site_header = "Metropolis administration"
admin.site.site_title = "Metropolis admin"
