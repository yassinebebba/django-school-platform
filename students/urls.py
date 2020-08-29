from django.urls import path
from .views import (
    student_home_view, profile_view, change_password_view, update_profile_view,
    ViewCourses, view_course_result, AnalysisView, course_analysis_view
)

app_name = 'students'

urlpatterns = [
    path('', student_home_view, name='student_home_view'),

    # student profile
    path('profile/', profile_view, name='profile_view'),
    path('profile/update-profile/', update_profile_view, name='update_profile_view'),
    path('profile/change-password/', change_password_view, name='change_password_view'),

    # courses
    path('view-courses/', ViewCourses.as_view(), name='view_courses'),
    path('view-courses/view-course-result/<str:course_name>/', view_course_result, name='view_course_result'),

    # analytics
    path('analysis/', AnalysisView.as_view(), name='analysis'),
    path('analysis/course-analysis/<str:course_name>/', course_analysis_view, name='course_analysis'),

]
