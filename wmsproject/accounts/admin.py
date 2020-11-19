from django.contrib import admin
from .models import User,HOD,Faculty,Student,TaskAssigned,Report
# Register your models here.


admin.site.register(User)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(HOD)
admin.site.register(TaskAssigned)
admin.site.register(Report)