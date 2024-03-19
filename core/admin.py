import django.db
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.messages import constants as messages
from django.db.models import Q
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from martor.widgets import AdminMartorWidget

from metropolis import settings

from . import models
from .forms import (
    AnnouncementAdminForm,
    AnnouncementSupervisorAdminForm,
    EventAdminForm,
    OrganizationAdminForm,
    TagAdminForm,
    TagSuperuserAdminForm,
    TermAdminForm,
    UserAdminForm,
)
from .models import Comment
from .utils.actions import *
from .utils.filters import (
    BlogPostAuthorListFilter,
    OrganizationListFilter,
    PostTypeFilter,
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
    list_display = ["name", "show_members", "is_open", "is_active", "owner"]
    list_filter = ["is_open", "show_members", "tags", "is_active"]
    fields = [
        "name",
        "bio",
        "extra_content",
        "slug",
        "show_members",
        "is_open",
        "is_active",
        "applications_open",
        "tags",
        "owner",
        "supervisors",
        "execs",
        "banner",
        "icon",
    ]
    autocomplete_fields = ["owner", "supervisors", "execs"]
    search_fields = ["name", "owner__username"]
    filter_horizontal = ("execs",)
    inlines = [
        TagInline,
        OrganizationURLInline,
    ]
    actions = [
        set_club_unactive,
        set_club_active,
        reset_club_president,
        reset_club_execs,
    ]
    form = OrganizationAdminForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(owner=request.user) | Q(execs=request.user)).distinct()

    def get_readonly_fields(self, request, obj=None):
        if obj is None or request.user.is_superuser or request.user == obj.owner:
            return []
        else:
            return ["owner", "supervisors", "execs", "is_active"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "supervisors" and not request.user.is_superuser:
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


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ["like_count", "save_count", "comments"]
    fields = ["like_count", "save_count", "comments"]

    def like_count(self, obj) -> int:
        return obj.like_count

    like_count.short_description = "Like count"

    def save_count(self, obj) -> int:
        saves = User.objects.filter(saved_announcements=obj).count()
        if saves is not None:
            return saves
        return 0

    save_count.short_description = "Save Count"

    def comments(self, obj):
        objs = list(
            map(
                lambda obj: '<a target="_blank" href="/admin/core/comment/%s">%s</a>'
                % (obj.pk, obj.body[:10]),
                obj.comments.all(),
            )
        )
        return mark_safe(",".join(objs))

    comments.short_description = "Comments"

    class Meta:
        abstract = True


class AnnouncementAdmin(PostAdmin):
    list_display = ["__str__", "organization", "status"]
    list_filter = [OrganizationListFilter, "status"]
    ordering = ["-show_after"]
    actions = [resend_approval_email]
    empty_value_display = "Not specified."
    formfield_overrides = {
        django.db.models.TextField: {"widget": AdminMartorWidget},
    }

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return (
            qs.filter(
                Q(organization__supervisors=request.user)
                | Q(organization__execs=request.user)
            )
            .distinct()
            .filter(organization__is_active=True)
        )

    def get_form(self, request, obj=None, **kwargs):
        kwargs["form"] = (
            AnnouncementSupervisorAdminForm
            if request.user.is_superuser or request.user.is_teacher
            else AnnouncementAdminForm
        )
        return super().get_form(request, obj, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is None or request.user.is_superuser:
            return PostAdmin.readonly_fields

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
        status_idx = ["d", "p", "a", "r"].index(obj.status)

        fields = set(all_fields)
        fields_matrix = [
            [
                {"author", "organization", "title", "tags", "is_public", "supervisor"},
                {"author", "organization", "title", "tags", "is_public", "supervisor"},
                {
                    "author",
                    "organization",
                    "title",
                    "body",
                    "tags",
                    "show_after",
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
                {"author", "organization", "supervisor"},
                {"author", "organization", "status", "supervisor"},
                {"author", "organization", "status", "show_after", "supervisor"},
                {"author", "organization", "status", "supervisor", "rejection_reason"},
            ],
        ]

        if request.user in obj.organization.supervisors.all():
            fields.intersection_update(fields_matrix[0][status_idx])
        if request.user in obj.organization.execs.all():
            fields.intersection_update(fields_matrix[1][status_idx])

        fields = list(fields)
        fields.sort(key=lambda x: all_fields.index(x))
        fields.extend(PostAdmin.readonly_fields)

        return fields

    def get_fields(self, request, obj=None):
        all_fields = [
            "organization",
            "author",
            "title",
            "body",
            "tags",
            "show_after",
            "is_public",
            "status",
            "rejection_reason",
            "supervisor",
        ]

        fields = set(all_fields)
        fields.difference_update(self.get_exclude(request, obj))

        fields = list(fields)
        fields.sort(key=lambda x: all_fields.index(x))
        if obj and obj.pk:
            fields.extend(PostAdmin.fields)

        return fields

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return {}

        if obj is None:
            return {"author", "supervisor", "rejection_reason"}

        status_idx = ["d", "p", "a", "r"].index(obj.status)

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
        elif (
            db_field.name in {"author", "supervisor"} and not request.user.is_superuser
        ):
            orgs = models.Organization.objects.filter(
                Q(supervisors=request.user) | Q(execs=request.user)
            )
            qs_set = True
            if db_field.name == "author":
                kwargs["queryset"] = models.User.objects.filter(
                    organizations_leading__in=orgs,
                )
                if request.user.is_superuser:
                    kwargs["queryset"] = models.User.objects.all()
            elif db_field.name == "supervisor":
                kwargs["queryset"] = models.User.objects.filter(
                    organizations_supervising__in=orgs,
                )
            else:
                qs_set = False
            if qs_set:
                kwargs["queryset"] = kwargs["queryset"].distinct().order_by("username")
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
            obj is not None
            and obj.status not in ("d", "p")
            and not request.user.is_superuser
            and request.user in obj.organization.supervisors.all()
            and request.user not in obj.organization.execs.all()
        ):
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        notify_supervisors = False

        if not request.user.is_superuser:
            if request.user in obj.organization.supervisors.all():
                obj.supervisor = request.user
                if obj.status not in ("d", "p") and request.user != obj.author:
                    # Notify author
                    self.message_user(
                        request,
                        f"Successfully marked announcement as {obj.get_status_display()}.",
                    )
            else:
                if (not change) or obj.status not in ("d", "p"):
                    notify_supervisors = True

                    self.message_user(
                        request, f"Successfully sent announcement for review."
                    )
                obj.status = "p" if obj.status != "d" else "d"

        super().save_model(request, obj, form, change)

        if notify_supervisors:
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


class BlogPostAdmin(PostAdmin):
    list_display = ["title", "author", "is_published", "views", "is_archived"]
    list_filter = [BlogPostAuthorListFilter, "is_published", "is_archived"]
    ordering = ["-show_after", "views"]
    fields = [
        "author",
        "title",
        "slug",
        "views",
        "body",
        "featured_image",
        "featured_image_description",
        "show_after",
        "tags",
        "is_published",
    ]
    readonly_fields = PostAdmin.readonly_fields
    formfield_overrides = {
        django.db.models.TextField: {"widget": AdminMartorWidget},
    }
    actions = [set_post_archived, set_post_unarchived]

    def get_fields(self, request, obj=None):
        if obj and obj.pk:
            return self.fields + PostAdmin.fields
        return self.fields

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


class ExhibitAdmin(PostAdmin):
    list_display = ["title", "author", "is_published"]
    list_filter = [BlogPostAuthorListFilter, "is_published"]
    ordering = ["-show_after"]
    fields = [
        "author",
        "title",
        "slug",
        "content",
        "content_description",
        "show_after",
        "tags",
        "is_published",
    ] + PostAdmin.fields
    readonly_fields = PostAdmin.readonly_fields
    formfield_overrides = {
        django.db.models.TextField: {"widget": AdminMartorWidget},
    }

    def get_changeform_initial_data(self, request):
        return {"author": request.user.pk}

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "tags":
            kwargs["queryset"] = (
                models.Tag.objects.filter(Q(organization=None))
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
            obj is not None
            and (not request.user.is_superuser)
            and (request.user not in obj.organization.execs.all())
        ):
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not all(
            map(
                lambda date: obj.term.start_datetime()
                <= date
                <= obj.term.end_datetime(),
                [obj.start_date, obj.end_date],
            )
        ):
            self.message_user(
                request,
                _("Event timeframe does not overlap term timeframe."),
                level=messages.ERROR,
            )
        super().save_model(request, obj, form, change)


class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "is_superuser", "is_staff", "is_teacher"]
    list_filter = [
        "is_superuser",
        "is_staff",
        "is_teacher",
        "groups",
        "graduating_year",
    ]
    search_fields = [
        "username",
        "first_name",
        "last_name",
        "saved_blogs__title",
        "saved_announcements__title",
    ]
    actions = [send_test_notif, send_notif_singleday, reset_password]
    action_form = AdminPasswordResetForm  # admin reset password form
    form = UserAdminForm

    def has_view_permission(self, request, obj=None):
        if obj is None and (
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


class CustomFlatPageAdmin(FlatPageAdmin):
    formfield_overrides = {
        django.db.models.TextField: {"widget": AdminMartorWidget},
    }
    actions = [archive_page]
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


class RaffleAdmin(admin.ModelAdmin):
    list_display = ["__str__", "open_start", "open_end"]


class CommentAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django.db.models.TextField: {"widget": AdminMartorWidget},
    }
    list_display = ["author", "content_object", "created_at"]
    search_fields = ["author__username", "body"]
    actions = [approve_comments, unapprove_comments]
    readonly_fields = ["created_at", "likes"]
    list_filter = ["live", PostTypeFilter]
    actions_on_top = True
    actions_on_bottom = True
    date_hierarchy = "created_at"

    def likes(self, obj: Comment):
        return obj.like_count

    def get_queryset(self, request):
        return Comment.objects.filter(author__isnull=False).order_by("-created_at")

    def content_object(self, obj):
        url = reverse(
            f"admin:{obj.content_type.app_label}_{obj.content_type.model}_change",
            args=[obj.object_id],
        )
        return format_html('<a href="{}">{}</a>', url, str(obj.content_object))

    content_object.short_description = "Associated Post"


admin.site.register(User, UserAdmin)
admin.site.register(models.Timetable, TimetableAdmin)
admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.Announcement, AnnouncementAdmin)
admin.site.register(models.BlogPost, BlogPostAdmin)
admin.site.register(models.Exhibit, ExhibitAdmin)
# admin.site.register(models.Comment, CommentAdmin) atm it's not used, so we don't need it
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Raffle, RaffleAdmin)

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, CustomFlatPageAdmin)

admin.site.site_header = "Metropolis administration"
admin.site.site_title = "Metropolis admin"
