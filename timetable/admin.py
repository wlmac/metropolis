from django.contrib import admin
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.


admin.site.register(User)
admin.site.register(models.Timetable)
admin.site.register(models.Course)
admin.site.register(models.School)
admin.site.register(models.Term)
