from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model
from django.forms import Textarea
from django.db.models import Q
import django.db

User = get_user_model()

# Register your models here.

class TermInline(admin.TabularInline):
    formfield_overrides = {
        django.db.models.TextField: {'widget': Textarea(attrs={'rows': 1})},
    }
    fields = ['name', 'num_courses', 'timetable_format', 'start_date', 'end_date']
    ordering = ['start_date']
    model = models.Term
    extra = 0

class EventInline(admin.StackedInline):
    ordering = ['start_date']
    model = models.Event
    extra = 0

class CourseInline(admin.TabularInline):
    formfield_overrides = {
        django.db.models.TextField: {'widget': Textarea(attrs={'rows': 1})},
    }
    fields = ['code', 'position', 'description']
    ordering = ['code']
    model = models.Course
    extra = 0

class TermAdmin(admin.ModelAdmin):
    inlines = [
        EventInline,
        CourseInline,
    ]

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_open', 'owner']
    list_filter = ['is_open', 'tags']
    fields = ['name', 'description', 'is_open', 'tags', 'owner', 'supervisors', 'execs']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(owner=request.user) | Q(execs=request.user)).distinct()

    def get_readonly_fields(self, request, obj=None):
        if obj == None or request.user.is_superuser or request.user == obj.owner:
            return []
        else:
            return ['owner', 'supervisors', 'execs']

class OrganizationListFilter(admin.SimpleListFilter):
    title = 'organization'
    parameter_name = 'org'

    def lookups(self, request, model_admin):
        qs = models.Organization.objects.filter(Q(owner=request.user) | Q(supervisors=request.user) | Q(execs=request.user)).distinct()
        for org in qs:
            yield (org.pk, org.name)

    def queryset(self, request, queryset):
        if self.value() == None or request.user.is_superuser:
            return queryset
        else:
            return queryset.filter(organization__slug=self.value())

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'organization', 'status']
    list_filter = [OrganizationListFilter, 'status']
    empty_value_display = "Not specified."

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(Q(organization__owner=request.user) | Q(organization__supervisors=request.user) | Q(organization__execs=request.user)).distinct()

    def get_readonly_fields(self, request, obj=None):
        if obj == None or request.user.is_superuser:
            return []

        all_fields = ['organization', 'author', 'title', 'body', 'tags', 'is_public', 'status', 'rejection_reason', 'supervisor']
        status_idx = ['p', 'a', 'r'].index(obj.status)

        fields = set(all_fields)
        fields_matrix = [
            [{'author', 'organization', 'title', 'body', 'tags', 'is_public'}, {'author', 'organization', 'title', 'body', 'tags', 'is_public', 'status', 'supervisor'}, {'author', 'organization', 'title', 'body', 'tags', 'is_public', 'status', 'rejection_reason', 'supervisor'}],
            [{'author', 'organization', 'status'}, {'author', 'organization', 'status', 'supervisor'}, {'author', 'organization', 'status', 'supervisor', 'rejection_reason'}],
        ]

        if request.user in obj.organization.supervisors.all():
            fields.intersection_update(fields_matrix[0][status_idx])
        if request.user in obj.organization.execs.all():
            fields.intersection_update(fields_matrix[1][status_idx])

        fields = list(fields)
        fields.sort(key=lambda x:all_fields.index(x))

        return fields

    def get_fields(self, request, obj=None):
        all_fields = ['organization', 'author', 'title', 'body', 'tags', 'is_public', 'status', 'rejection_reason', 'supervisor']

        fields = set(all_fields)
        fields.difference_update(self.get_exclude(request, obj))

        fields = list(fields)
        fields.sort(key=lambda x:all_fields.index(x))

        return fields

    def get_exclude(self, request, obj=None):
        if request.user.is_superuser:
            return {}

        if obj == None:
            return {'author', 'supervisor', 'status', 'rejection_reason'}

        status_idx = ['p', 'a', 'r'].index(obj.status)

        fields = {'title', 'body', 'tags', 'organization', 'is_public', 'supervisor', 'status', 'rejection_reason'}
        fields_matrix = [
            [{'supervisor'}, {'rejection_reason'}, {}],
            [{'supervisor', 'rejection_reason'}, {'rejection_reason'}, {}],
        ]

        if request.user in obj.organization.supervisors.all():
            fields.intersection_update(fields_matrix[0][status_idx])
        if request.user in obj.organization.execs.all():
            fields.intersection_update(fields_matrix[1][status_idx])

        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "organization":
            if not request.user.is_superuser:
                kwargs["queryset"] = models.Organization.objects.filter(Q(supervisors=request.user) | Q(execs=request.user)).distinct()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if obj != None and obj.status != 'p' and request.user in obj.organization.supervisors.all() and request.user not in obj.organization.execs.all():
            return False
        return super().has_change_permission(request, obj)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user

        if request.user in obj.organization.supervisors.all():
            obj.supervisor = request.user
            if obj.status != 'p' and request.user != obj.author:
                # Notify user
                pass
                self.message_user(request, f'Successfully marked announcement as {obj.get_status_display()}.')
        else:
            if obj.status != 'p':
                # Notify supervisors
                self.message_user(request, f'Successfully sent announcement for review.')
            obj.status = 'p'

        super().save_model(request, obj, form, change)

admin.site.register(User)
admin.site.register(models.Timetable)
admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.Announcement, AnnouncementAdmin)
admin.site.register(models.Tag)

admin.site.site_header = "Metropolis administration"
admin.site.site_title = "Metropolis admin"
