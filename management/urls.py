from django.urls import path
from .views import (
    administration_view, profile_view, UpdateProfile, change_password_view,
    create_student, StudentsView, edit_student,
    create_teacher, TeachersView, edit_teacher,
    UserDelete,
    create_course, CoursesView, EditCourse, DeleteCourse,
    create_grade_level, GradeLevelsView, EditGradeLevel, DeleteGradeLevel,
    create_grade_class, GradeClassesView, EditGradeClass, DeleteGradeClass,
    create_academic_term, AcademicTermsView, EditAcademicTerm, DeleteAcademicTerm,
    view_database,
)

app_name = 'management'

urlpatterns = [
    path('', administration_view, name='administration_view'),

    # admin profile
    path('profile/', profile_view, name='profile_view'),
    path('profile/<int:pk>/update-profile/', UpdateProfile.as_view(), name='update_profile_view'),
    path('profile/change-password/', change_password_view, name='change_password_view'),

    # student related paths
    path('create-student/', create_student, name='create_student'),
    path('view-database/view-students/', StudentsView.as_view(), name='view_students'),
    path('view-database/view-students/<int:student_id>/', edit_student, name='edit_student'),

    # teacher related paths
    path('create-teacher/', create_teacher, name='create_teacher'),
    path('view-database/view-teachers/', TeachersView.as_view(), name='view_teachers'),
    path('view-database/view-teachers/<int:teacher_id>', edit_teacher, name='edit_teacher'),

    # student and teacher delete path
    path('delete-user/<int:pk>/', UserDelete.as_view(), name='delete_user'),

    # course related paths
    path('create-course/', create_course, name='create_course'),
    path('view-database/view-courses/', CoursesView.as_view(), name='view_courses'),
    path('view-database/view-courses/<int:pk>/edit-course/', EditCourse.as_view(), name='edit_course'),
    path('view-database/view-courses/<int:pk>/delete-course/', DeleteCourse.as_view(), name='delete_course'),

    # grade level related paths
    path('create-grade-level/', create_grade_level, name='create_grade_level'),
    path('view-database/view-grade-levels/', GradeLevelsView.as_view(), name='view_grade_levels'),
    path('view-database/view-grade-levels/<int:pk>/edit-grade-level/', EditGradeLevel.as_view(),
         name='edit_grade_level'),
    path('view-database/view-grade-levels/<int:pk>/delete-grade-level/', DeleteGradeLevel.as_view(),
         name='delete_grade_level'),

    # grade class related paths
    path('create-grade-class/', create_grade_class, name='create_grade_class'),
    path('view-database/view-grade-classes/', GradeClassesView.as_view(), name='view_grade_classes'),
    path('view-database/view-grade-classes/<int:pk>/edit-grade-class/', EditGradeClass.as_view(),
         name='edit_grade_class'),
    path('view-database/view-grade-classes/<int:pk>/delete-grade-class/', DeleteGradeClass.as_view(),
         name='delete_grade_class'),

    # academic term related paths
    path('create-academic-term/', create_academic_term, name='create_academic_term'),
    path('view-database/view-academic-terms/', AcademicTermsView.as_view(), name='view_academic_terms'),
    path('view-database/view-academic-terms/<int:pk>/edit-academic-term/', EditAcademicTerm.as_view(),
         name='edit_academic_term'),
    path('view-database/view-academic-terms/<int:pk>/delete-academic-term/', DeleteAcademicTerm.as_view(),
         name='delete_academic_term'),

    # view database
    path('view-database/', view_database, name='view_database'),
]
