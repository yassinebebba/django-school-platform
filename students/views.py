from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views.generic import UpdateView, DetailView
from django.contrib import messages
from management.models import Account
from django.core.exceptions import ObjectDoesNotExist
from .decorators import student_only
from django.views.generic import ListView
from .forms import StudentInfoUpdateForm, StudentAccountUpdateForm
from management.forms import ChangePasswordForm
from django.utils import timezone
from students.models import Student, ExamGrade


@permission_required('management.is_student', raise_exception=Http404)
@login_required(login_url='main:login')
def student_home_view(request):
    return render(request, 'students/home.html')


class ViewCourses(PermissionRequiredMixin, ListView):
    permission_required = 'management.is_student'
    login_url = Http404
    template_name = 'students/view_courses.html'
    model = Account
    context_object_name = 'courses'

    def get_queryset(self):
        # return self.request.user.student.grade_class.course.all()
        return Account.objects.get(pk=self.request.user.id).student.grade_class.course.all()


@permission_required('management.is_student', raise_exception=Http404)
@login_required(login_url='main:login')
def view_course_result(request, course_name):
    try:
        request.user.student.grade_class.course.get(course_name=course_name)
    except ObjectDoesNotExist:
        raise Http404
    course_results = request.user.student.examgrade_set.filter(exam_course=course_name,
                                                               exam__exam_creation_date__lte=timezone.now()
                                                               ).order_by('-exam__exam_creation_date')
    context = {
        'course_name': course_name,
        'course_results': course_results
    }
    return render(request, 'students/view_course_result.html', context=context)


@permission_required('management.is_student', raise_exception=Http404)
@login_required(login_url='main:login')
def profile_view(request):
    return render(request, 'students/profile.html')


@permission_required('management.is_student', raise_exception=Http404)
@login_required(login_url='main:login')
def update_profile_view(request):
    if request.method == 'POST':
        account_form = StudentAccountUpdateForm(request.POST, instance=request.user)
        info_form = StudentInfoUpdateForm(request.POST, instance=request.user.student)
        if account_form.is_valid() and info_form.is_valid():
            account_form.save()
            info_form.save()
            messages.success(request, 'Profile has been updated.')
            return HttpResponseRedirect(reverse('main:students:profile_view'))
    else:
        account_form = StudentAccountUpdateForm(instance=request.user)
        info_form = StudentInfoUpdateForm(instance=request.user.student)
    context = {
        'account_form': account_form,
        'info_form': info_form,
    }
    return render(request, 'students/update_profile.html', context=context)


@permission_required('management.is_student', raise_exception=Http404)
@login_required(login_url='main:login')
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['password2']
            if not request.user.check_password(current_password):
                messages.warning(request, 'Incorrect password')
                return render(request, 'students/change_password.html', context={'form': form})
            user = request.user
            user.set_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, 'Your password has been changed.')
            return redirect('main:students:profile_view')
    else:
        form = ChangePasswordForm()
    return render(request, 'students/change_password.html', context={'form': form})


class AnalysisView(PermissionRequiredMixin, ListView):
    permission_required = 'management.is_student'
    login_url = Http404
    template_name = 'students/analysis.html'
    model = Account
    context_object_name = 'courses'

    def get_queryset(self):
        # return self.request.user.student.grade_class.course.all()
        return Account.objects.get(pk=self.request.user.id).student.grade_class.course.all()


@permission_required('management.is_student', raise_exception=Http404)
@login_required(login_url='main:login')
def course_analysis_view(request, course_name):
    try:
        request.user.student.grade_class.course.get(course_name=course_name)
    except ObjectDoesNotExist:
        raise Http404
    course_results = request.user.student.examgrade_set.filter(exam_course=course_name,
                                                               exam__exam_creation_date__lte=timezone.now()
                                                               ).order_by('exam__exam_creation_date')
    context = {
        'course_name': course_name,
        'course_results': course_results
    }
    return render(request, 'students/course_analysis.html', context=context)
