from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    Account, GradeLevel, GradeClass, Course
)

from .forms import (
    UserCreationForm, UserChangeForm
)


class UserAdmin(BaseUserAdmin):
    readonly_fields = ('modified',)

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('identifier', 'first_name', 'last_name', 'email', 'is_superuser')
    list_filter = ('is_active', 'is_student', 'is_teacher', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'gender', 'date_added', 'modified')}),
        ('Permissions', {'fields': ('is_active', 'is_student', 'is_teacher', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2', 'gender', 'date_added',
                'is_active', 'is_student', 'is_teacher', 'is_staff', 'is_superuser'),
        }),
    )
    search_fields = ('first_name',)
    ordering = ('identifier',)
    filter_horizontal = ()


admin.site.register(Account, UserAdmin)
admin.site.register(GradeLevel)
admin.site.register(GradeClass)
admin.site.register(Course)
admin.site.unregister(Group)
