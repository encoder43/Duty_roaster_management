from django.contrib import admin
from django.contrib.admin import site
from .models import *
# Register your models here.

admin.site.register(EmployeeDetail)
admin.site.register(Attendance)
admin.site.register(Request)
admin.site.register(Announcement)
admin.site.register(Shift)
