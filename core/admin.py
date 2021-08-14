from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model
from django.forms import Textarea
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

admin.site.register(User)
admin.site.register(models.Timetable)
admin.site.register(models.Term, TermAdmin)
