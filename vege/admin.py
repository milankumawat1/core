from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Recipie)

admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Subject)

class SubjectMarksAdmin(admin.ModelAdmin):
    list_display=['student','subject','marks']


    
admin.site.register(SubjectMarks , SubjectMarksAdmin)





