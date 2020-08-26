from django.shortcuts import render


def student_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_student:
            return render(request, 'students/home.html')
        else:
            return func(request, *args, **kwargs)
    return wrapper
