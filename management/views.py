from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse
from django.views.generic import DeleteView, ListView, UpdateView

from .models import (
    Account, Course, GradeLevel, GradeClass, AcademicTerm
)
from django.contrib.auth import login
from students.models import Student
from teachers.models import Teacher
from .forms import (
    StudentCreationForm, StudentAccountUpdateForm, StudentInfoUpdateForm,
    TeacherCreationForm, TeacherAccountUpdateForm, TeacherInfoUpdateForm,
    CourseCreationForm, GradeLevelCreationForm, GradeClassCreationForm, AcademicTermCreationForm,
    ChangePasswordForm,
)
from django.contrib.auth.models import Permission


@permission_required('is_superuser', raise_exception=Http404)
@login_required(login_url='main:login')
def administration_view(request):
    return render(request, 'management/home.html')


@permission_required('is_superuser', raise_exception=Http404)
@login_required(login_url='main:login')
def profile_view(request):
    return render(request, 'management/admin/profile.html')


class UpdateProfile(PermissionRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = Account
    queryset = Account.objects.filter(is_superuser=True)
    template_name = 'management/admin/update_profile.html'
    fields = ('email', 'first_name', 'last_name', 'gender',)

    def test_func(self):
        if self.request.user == self.get_object():
            return True
        return False

    def get_success_url(self):
        return reverse('main:management:profile_view')

    def get_success_message(self, cleaned_data):
        return f'Profile has been updated successfully.'


@permission_required('is_superuser', raise_exception=Http404)
@login_required(login_url='main:login')
def change_password_view(request):
    """
    PLEASE NOTE: THE CHANGE ADMIN PASSWORD VIEW WORKS FOR NOW,
    BUT I HAVE NO IDEA IF THE SOLUTION IS IDEAL OR NOT
    PLEASE CHECK IT.
    give this to Rainer to check if it works for single object or not,
    without using user_passes_test
    """
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['password2']
            if not request.user.check_password(current_password):
                messages.warning(request, 'Incorrect password')
                return render(request, 'management/admin/change_password.html', context={'form': form})
            user = request.user
            user.set_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, 'Your password has been changed.')
            return redirect('main:management:profile_view')
    else:
        form = ChangePasswordForm()
    return render(request, 'management/admin/change_password.html', context={'form': form})


def get_user_info(email):
    return Account.objects.get(email=email)


@permission_required('is_superuser', raise_exception=Http404)
@login_required(login_url='main:login')
def create_student(request):
    """ Create a new student in the Database """

    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            fist_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']
            grade_class = form.cleaned_data['grade_class']

            # abstract common info
            phone_number = form.cleaned_data['phone_number']
            address_line_1 = form.cleaned_data['address_line_1']
            address_line_2 = form.cleaned_data['address_line_2']
            postcode = form.cleaned_data['postcode']

            # guardian info
            guardian_first_name = form.cleaned_data['guardian_first_name']
            guardian_last_name = form.cleaned_data['guardian_last_name']
            guardian_relationship = form.cleaned_data['guardian_relationship']
            guardian_phone_number = form.cleaned_data['guardian_phone_number']

            # notes
            notes = form.cleaned_data['notes']

            student = Account(email=email, first_name=fist_name, last_name=last_name, gender=gender)
            student.is_student = True
            student.make_random_password(instance=student, length=10,
                                         allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            student.save()
            Student.objects.create(account=student,
                                   date_of_birth=date_of_birth,
                                   grade_class=grade_class,
                                   address_line_1=address_line_1,
                                   address_line_2=address_line_2,
                                   postcode=postcode,
                                   phone_number=phone_number,
                                   guardian_first_name=guardian_first_name,
                                   guardian_last_name=guardian_last_name,
                                   guardian_relationship=guardian_relationship,
                                   guardian_phone_number=guardian_phone_number,
                                   notes=notes
                                   )
            management_permissions = Permission.objects.filter(content_type__app_label='management',
                                                               content_type__model='account')
            student_perm = management_permissions.get(codename='is_student')
            student.user_permissions.add(student_perm)

            student.save()

            user_id = get_user_info(email).identifier
            messages.success(request, f'Student {fist_name} {last_name} with ID ({user_id}), '
                                      f'has been successfully added.')
            return redirect('main:management:create_student')
    else:
        form = StudentCreationForm()

    return render(request, 'management/create_student.html', context={'form': form})


@permission_required('is_superuser', raise_exception=Http404)
def edit_student(request, student_id):
    account_obj = get_object_or_404(Account.objects.filter(is_student=True), pk=student_id)
    if request.method == 'POST':
        account_form = StudentAccountUpdateForm(request.POST, instance=account_obj)
        info_form = StudentInfoUpdateForm(request.POST, instance=account_obj.student)
        if account_form.is_valid() and info_form.is_valid():
            account_form.save()
            info_form.save()
            messages.success(request, 'Student account has been updated.')
            return HttpResponseRedirect(reverse('main:management:edit_student', args=(student_id,)))
    else:
        account_form = StudentAccountUpdateForm(instance=account_obj)
        info_form = StudentInfoUpdateForm(instance=account_obj.student)
    context = {
        'account_form': account_form,
        'info_form': info_form,
        'object': account_obj,
        'student_id': student_id
    }
    return render(request, 'management/edit_student.html', context=context)


@permission_required('is_superuser', raise_exception=Http404)
def create_teacher(request):
    """ Create a new student in the Database """

    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            fist_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            gender = form.cleaned_data['gender']
            date_of_birth = form.cleaned_data['date_of_birth']
            grade_class = form.cleaned_data['grade_class']
            course = form.cleaned_data['course']

            # abstract common info
            phone_number = form.cleaned_data['phone_number']
            address_line_1 = form.cleaned_data['address_line_1']
            address_line_2 = form.cleaned_data['address_line_2']
            postcode = form.cleaned_data['postcode']

            teacher = Account(email=email, first_name=fist_name, last_name=last_name, gender=gender)
            teacher.is_teacher = True
            teacher.make_random_password(instance=teacher, length=10,
                                         allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
            grade_class_gen = (GradeClass.objects.get(pk=id) for id in grade_class)
            teacher.save()
            course_obj = Course.objects.get(pk=course)
            teacher_obj = Teacher(account=teacher,
                                  course=course_obj,
                                  date_of_birth=date_of_birth,
                                  address_line_1=address_line_1,
                                  address_line_2=address_line_2,
                                  postcode=postcode,
                                  phone_number=phone_number,
                                  )
            teacher_obj.save()
            for i in grade_class_gen:
                teacher_obj.grade_class.add(i)
                teacher_obj.save()
            management_permissions = Permission.objects.filter(content_type__app_label='management',
                                                               content_type__model='account')
            teacher_perm = management_permissions.get(codename='is_teacher')
            teacher.user_permissions.add(teacher_perm)

            teacher.save()

            user_id = get_user_info(email).identifier
            messages.success(request, f'Teacher {fist_name} {last_name} with ID ({user_id}), '
                                      f'has been successfully added.')
            return redirect('main:management:create_teacher')
    else:
        form = TeacherCreationForm()

    return render(request, 'management/create_teacher.html', context={'form': form})


@permission_required('is_superuser', raise_exception=Http404)
def edit_teacher(request, teacher_id):
    account_obj = get_object_or_404(Account.objects.filter(is_teacher=True), pk=teacher_id)
    if request.method == 'POST':
        account_form = TeacherAccountUpdateForm(request.POST, instance=account_obj)
        info_form = TeacherInfoUpdateForm(request.POST, instance=account_obj.teacher)
        if account_form.is_valid() and info_form.is_valid():
            account_form.save()
            info_form.save()
            messages.success(request, 'Teacher account has been updated.')
            return HttpResponseRedirect(reverse('main:management:edit_teacher', args=(teacher_id,)))
    else:
        account_form = TeacherAccountUpdateForm(instance=account_obj)
        info_form = TeacherInfoUpdateForm(instance=account_obj.teacher)
    context = {
        'account_form': account_form,
        'info_form': info_form,
        'object': account_obj,
        'teacher_id': teacher_id
    }
    return render(request, 'management/edit_teacher.html', context=context)


# links to users in the database
@permission_required('is_superuser', raise_exception=Http404)
def view_database(request):
    return render(request, 'management/view_database.html')


class StudentsView(PermissionRequiredMixin, ListView):
    """ filter all students from the Database and view them """

    permission_required = 'is_superuser'
    raise_exception = Http404
    model = Account
    template_name = 'management/view_students.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        accounts = Account.objects.filter(is_student=True)
        return accounts.order_by('-identifier')


class TeachersView(PermissionRequiredMixin, ListView):
    """ filter all teachers from the Database and view them """

    permission_required = 'is_superuser'
    raise_exception = Http404
    model = Account
    template_name = 'management/view_teachers.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        accounts = Account.objects.filter(is_teacher=True)
        return accounts.order_by('-identifier')


class UserDelete(PermissionRequiredMixin, DeleteView):
    """ get the user's id and pass it to the DeleteView """

    permission_required = 'is_superuser'
    raise_exception = Http404
    model = Account
    template_name = 'management/account_confirm_delete.html'

    def get_success_url(self):
        return reverse('main:management:view_database')


# Course related views
@permission_required('is_superuser', raise_exception=Http404)
def create_course(request):
    if request.method == 'POST':
        form = CourseCreationForm(request.POST)
        if form.is_valid():
            form.save()
            course_name = form.cleaned_data['course_name']
            messages.success(request, f'Course {course_name} has been created successfully.')
            return redirect('main:management:create_course')
    else:
        form = CourseCreationForm()

    return render(request, 'management/courses/create_course.html', context={'form': form})


class CoursesView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = Course
    template_name = 'management/courses/view_courses.html'
    context_object_name = 'courses'

    def get_queryset(self):
        return Course.objects.all()


class EditCourse(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = Course
    template_name = 'management/courses/edit_course.html'
    fields = ('course_name',)

    def get_success_url(self):
        return reverse('main:management:view_courses')

    def get_success_message(self, cleaned_data):
        return f'Course {self.object.course_name} has been updated successfully.'


class DeleteCourse(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """ get the course's id and pass it to the DeleteView """

    permission_required = 'is_superuser'
    raise_exception = Http404
    model = Course
    template_name = 'management/courses/course_confirm_delete.html'

    def get_success_url(self):
        return reverse('main:management:view_courses')

    def get_success_message(self, cleaned_data):
        return f'Course {self.object.course_name} has been deleted successfully.'


# Grade Level related views
@permission_required('is_superuser', raise_exception=Http404)
def create_grade_level(request):
    if request.method == 'POST':
        form = GradeLevelCreationForm(request.POST)
        if form.is_valid():
            form.save()
            grade_level_name = form.cleaned_data['grade_level_name']
            messages.success(request, f'Grade level {grade_level_name} has been created successfully.')
            return redirect('main:management:create_grade_level')
    else:
        form = GradeLevelCreationForm()

    return render(request, 'management/grade_levels/create_grade_level.html', context={'form': form})


class GradeLevelsView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = GradeLevel
    template_name = 'management/grade_levels/view_grade_levels.html'
    context_object_name = 'grade_levels'

    def get_queryset(self):
        return GradeLevel.objects.all()


class EditGradeLevel(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = GradeLevel
    template_name = 'management/grade_levels/edit_grade_level.html'
    fields = ('grade_level_name',)

    def get_success_url(self):
        return reverse('main:management:view_grade_levels')

    def get_success_message(self, cleaned_data):
        return f'Course {self.object.grade_level_name} has been updated successfully.'


class DeleteGradeLevel(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """ get the grade level's id and pass it to the DeleteView """

    permission_required = 'is_superuser'
    raise_exception = Http404
    model = GradeLevel
    template_name = 'management/grade_levels/grade_level_confirm_delete.html'

    def get_success_url(self):
        return reverse('main:management:view_grade_levels')

    def get_success_message(self, cleaned_data):
        return f'Course {self.object.grade_level_name} has been deleted successfully.'


# Grade class related views
@permission_required('is_superuser', raise_exception=Http404)
def create_grade_class(request):
    if request.method == 'POST':
        form = GradeClassCreationForm(request.POST)
        if form.is_valid():
            form.save()
            grade_class_name = form.cleaned_data['grade_class_name']
            messages.success(request, f'Grade class {grade_class_name} has been created successfully.')
            return redirect('main:management:create_grade_class')
    else:
        form = GradeClassCreationForm()

    return render(request, 'management/grade_classes/create_grade_class.html', context={'form': form})


class GradeClassesView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = GradeClass
    template_name = 'management/grade_classes/view_grade_classes.html'
    context_object_name = 'grade_classes'

    def get_queryset(self):
        return GradeClass.objects.all()


class EditGradeClass(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = GradeClass
    template_name = 'management/grade_classes/edit_grade_class.html'
    fields = ('grade_class_name', 'grade_level', 'course',)

    def get_success_url(self):
        return reverse('main:management:view_grade_classes')

    def get_success_message(self, cleaned_data):
        return f'Course {self.object.grade_class_name} has been updated successfully.'


class DeleteGradeClass(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """ get the grade class's id and pass it to the DeleteView """

    permission_required = 'is_superuser'
    raise_exception = Http404
    model = GradeClass
    template_name = 'management/grade_classes/grade_class_confirm_delete.html'

    def get_success_url(self):
        return reverse('main:management:view_grade_classes')

    def get_success_message(self, cleaned_data):
        return f'Course {self.object.grade_class_name} has been deleted successfully.'


# academic term related views
@permission_required('is_superuser', raise_exception=Http404)
def create_academic_term(request):
    if request.method == 'POST':
        form = AcademicTermCreationForm(request.POST)
        if form.is_valid():
            form.save()
            academic_term_name = form.cleaned_data['academic_term_name']
            messages.success(request, f'Academic term {academic_term_name} has been created successfully.')
            return redirect('main:management:create_academic_term')
    else:
        form = AcademicTermCreationForm()

    return render(request, 'management/academic_terms/create_academic_term.html', context={'form': form})


class AcademicTermsView(PermissionRequiredMixin, ListView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = AcademicTerm
    template_name = 'management/academic_terms/view_academic_terms.html'
    context_object_name = 'academic_terms'

    def get_queryset(self):
        filter_value = self.request.GET.get('filter', 'Year')
        if filter_value != 'None':
            new_context = AcademicTerm.objects.filter(academic_year__contains=filter_value)
        else:
            new_context = AcademicTerm.objects.all()

        return new_context

    def get_context_data(self, **kwargs):
        context = super(AcademicTermsView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', 'None')
        return context


class EditAcademicTerm(SuccessMessageMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    raise_exception = Http404
    model = AcademicTerm
    template_name = 'management/academic_terms/edit_academic_term.html'

    fields = ('academic_term_name', 'academic_term_multiplier', 'academic_year',)

    def get_success_url(self):
        return reverse('main:management:view_academic_terms')

    def get_success_message(self, cleaned_data):
        return f'Academic term {self.object.academic_term_name} has been updated successfully.'


class DeleteAcademicTerm(SuccessMessageMixin, PermissionRequiredMixin, DeleteView):
    """ get the grade class's id and pass it to the DeleteView """

    permission_required = 'is_superuser'
    raise_exception = Http404
    model = AcademicTerm
    template_name = 'management/academic_terms/academic_term_confirm_delete.html'

    def get_success_url(self):
        return reverse('main:management:view_academic_terms')

    def get_success_message(self, cleaned_data):
        return f'Academic term {self.object.academic_term_name} has been deleted successfully.'
