from django.contrib import admin
from .models import Teacher, Exam


class TeacherConfig(admin.ModelAdmin):
    readonly_fields = ('modified',)
    list_display = ('account',)
    search_fields = ('account__identifier',)


admin.site.register(Teacher, TeacherConfig)
admin.site.register(Exam)
