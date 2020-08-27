from django.urls import path, include, reverse_lazy

from .views import (
    landing_page_view, CustomLoginView, account_redirect
)
from django.contrib.auth.views import (
    LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
)
from django.conf.urls.static import static
from django.conf import settings

app_name = 'main'

urlpatterns = [
    path('', landing_page_view, name='landing_page'),
    path('login/', CustomLoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', account_redirect, name='account_redirect'),

    # password reset
    path('password-reset/',
         PasswordResetView.as_view(template_name='main/password_reset.html',
                                   success_url=reverse_lazy('main:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name='main/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         PasswordResetConfirmView.as_view(template_name='main/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='main/password_reset_complete.html'),
         name='password_reset_complete'),

    path('administration/', include(('management.urls', 'management'), namespace='management')),
    path('student/', include(('students.urls', 'students'), namespace='students')),
    path('teacher/', include(('teachers.urls', 'teachers'), namespace='teachers')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
