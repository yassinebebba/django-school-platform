from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required, login_required, user_passes_test
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.views.generic import UpdateView, DeleteView, DetailView
from django.contrib import messages
from management.models import Account
from students.models import ExamGrade
from .forms import TeacherAccountUpdateForm, TeacherInfoUpdateForm, ExamCreationForm
from management.forms import ChangePasswordForm
from .models import Teacher, Exam
from django.views.generic import ListView


@permission_required('management.is_teacher', raise_exception=Http404)
@login_required(login_url='main:login')
def teacher_home_view(request):
    return render(request, 'teachers/home.html')



@permission_required('management.is_teacher', raise_exception=Http404)
@login_required(login_url='main:login')
def profile_view(request):
    return render(request, 'teachers/profile.html')

@permission_required('management.is_teacher', raise_exception=Http404)
@login_required(login_url='main:login')
def update_profile_view(request):
    if request.method == 'POST':
        account_form = TeacherAccountUpdateForm(request.POST, instance=request.user)
        info_form = TeacherInfoUpdateForm(request.POST, instance=request.user.teacher)
        if account_form.is_valid() and info_form.is_valid():
            account_form.save()
            info_form.save()
            messages.success(request, 'Profile has been updated.')
            return HttpResponseRedirect(reverse('main:teachers:profile_view'))
    else:
        account_form = TeacherAccountUpdateForm(instance=request.user)
        info_form = TeacherInfoUpdateForm(instance=request.user.teacher)
    context = {
        'account_form': account_form,
        'info_form': info_form,
    }
    return render(request, 'teachers/update_profile.html', context=context)

@permission_required('management.is_teacher', raise_exception=Http404)
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
                return render(request, 'teachers/change_password.html', context={'form': form})
            user = request.user
            user.set_password(new_password)
            user.save()
            login(request, user)
            messages.success(request, 'Your password has been changed.')
            return redirect('main:teachers:profile_view')
    else:
        form = ChangePasswordForm()
    return render(request, 'teachers/change_password.html', context={'form': form})

@permission_required('management.is_teacher', raise_exception=Http404)
@login_required(login_url='main:login')
def add_assessment(request):
    if request.method == 'POST':
        form = ExamCreationForm(request.POST)
        if form.is_valid():
            prof = Teacher.objects.get(account=request.user.id)
            obj = form.save(commit=False)
            obj.teacher = prof
            obj.save()
            messages.success(request, 'Assessment has been added successfully')
            return redirect('main:teachers:view_assessments')
    else:
        form = ExamCreationForm()
    return render(request, 'teachers/add_assessment.html', context={'form': form})


class ViewAssessments(PermissionRequiredMixin, ListView):
    permission_required = 'management.is_teacher'
    login_url = Http404
    template_name = 'teachers/view_assessments.html'
    model = Exam
    context_object_name = 'assessments'

    def get_queryset(self):
        user = self.request.user
        teacher = Teacher.objects.get(account=Account.objects.get(id=user.id))
        query = Exam.objects.filter(teacher=teacher).order_by('-exam_creation_date')
        return query


class MarkStudents(PermissionRequiredMixin, DetailView):
    permission_required = 'management.is_teacher'
    login_url = Http404
    template_name = 'teachers/mark_students.html'
    model = Exam

class Mark(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'management.is_teacher'
    login_url = Http404
    template_name = 'teachers/mark.html'
    model = ExamGrade
    fields = ('grade_result', 'feedback',)

    def get_success_message(self, cleaned_data):
        return f'{self.object.student} has been updated successfully.'

    def get_success_url(self):
        return reverse('main:teachers:mark_students', args=(self.kwargs.get('id'),))



class EditAssessment(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'management.is_teacher'
    login_url = Http404
    template_name = 'teachers/edit_assessment.html'
    model = Exam
    fields = ('exam_name', 'grade_class', 'academic_term', 'exam_type', 'description',
              'exam_creation_date', 'exam_deadline', 'multiplier', 'full_mark')

    def get_success_message(self, cleaned_data):
        return f'{self.object.exam_name} has been updated successfully.'

    def get_success_url(self):
        return reverse('main:teachers:view_assessments')

class DeleteAssessment(PermissionRequiredMixin, SuccessMessageMixin, DeleteView):
    permission_required = 'management.is_teacher'
    login_url = Http404
    template_name = 'teachers/assessment_confirm_delete.html'
    model = Exam

    def get_success_message(self, cleaned_data):
        return f'{self.object.exam_name} has been deleted successfully.'

    def get_success_url(self):
        return reverse('main:teachers:view_assessments')