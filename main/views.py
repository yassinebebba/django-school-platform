from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from datetime import datetime

class CustomLoginView(SuccessMessageMixin, LoginView):

    def get_success_message(self, cleaned_data):
        date = datetime.now().hour
        if 5 <= date <= 11:
            return f'Good morning, { self.request.user.first_name } {self.request.user.last_name }.'
        elif 12 <= date <= 17:
            return f'Good afternoon, { self.request.user.first_name } {self.request.user.last_name }.'
        else:
            return f'Good evening, { self.request.user.first_name } {self.request.user.last_name }.'

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse('main:management:administration_view')
        elif self.request.user.is_student:
            return reverse('main:students:student_home_view')
        elif self.request.user.is_teacher:
            return reverse('main:teachers:teacher_home_view')

@login_required(login_url='main:login')
def account_redirect(request):
    if request.user.is_superuser:
        return redirect('main:management:administration_view')
    elif request.user.is_student:
        return redirect('main:students:student_home_view')
    elif request.user.is_teacher:
        return redirect('main:teachers:teacher_home_view')

# view of the first page of the website.
def landing_page_view(request):
    return render(request, 'main/landing_page.html')
