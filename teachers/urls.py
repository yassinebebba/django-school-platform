from django.urls import path
from .views import (
    teacher_home_view, profile_view, change_password_view, update_profile_view,
    add_assessment, ViewAssessments, MarkStudents, Mark, EditAssessment, DeleteAssessment
)

app_name = 'teachers'

urlpatterns = [
    path('', teacher_home_view, name='teacher_home_view'),

    # add assessment
    path('add-assessment/', add_assessment, name='add_assessment'),
    path('view-assessments/', ViewAssessments.as_view(), name='view_assessments'),
    path('view-assessments/<int:pk>/mark-students/', MarkStudents.as_view(), name='mark_students'),
    path('view-assessments/<int:id>/mark-students/<int:pk>', Mark.as_view(), name='mark'),
    path('view-assessments/<int:pk>/edit', EditAssessment.as_view(), name='edit_assessment'),
    path('view-assessments/<int:pk>/delete', DeleteAssessment.as_view(), name='delete_assessment'),
    # student profile
    path('profile/', profile_view, name='profile_view'),
    path('profile/update-profile/', update_profile_view, name='update_profile_view'),
    path('profile/change-password/', change_password_view, name='change_password_view'),
]
