from django.contrib import admin
from .models import *
from django.db.models import Sum
# Register your models here.
admin.site.register(Recipie)

admin.site.register(Department)
admin.site.register(StudentID)
admin.site.register(Student)
admin.site.register(Subject)


class SubjectMarksAdmin(admin.ModelAdmin):
    list_display=['student','subject','marks']


    
admin.site.register(SubjectMarks , SubjectMarksAdmin)

class ReportCardAdmin(admin.ModelAdmin):
    list_display=['student','student_rank','total_marks','date_of_report_card_generation']
    ordering=['student_rank']
    def total_marks(self,obj):
        subject_marks=SubjectMarks.objects.filter(student=obj.student)
        total_marks=subject_marks.aggregate(marks=Sum('marks'))
        return total_marks['marks']
admin.site.register(ReportCard,ReportCardAdmin)



