from django.contrib import admin
from .models import Student, ExamGrade

class StudentConfig(admin.ModelAdmin):
    readonly_fields = ('modified',)
    list_display = ('account', 'grade_class')
    search_fields = ('account__identifier',)


admin.site.register(Student, StudentConfig)
admin.site.register(ExamGrade)

