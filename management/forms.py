from .models import (
    Account, GradeClass, Course, GradeLevel, AcademicTerm
)
from students.models import Student
from teachers.models import Teacher
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField



class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('identifier', 'email', 'first_name', 'last_name', 'gender')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'gender', 'password')

    def clean_password(self):
        return self.initial["password"]

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(label='Current password', widget=forms.PasswordInput)
    password1 = forms.CharField(label='New password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='New password confirmation', widget=forms.PasswordInput)

    class Meta:
        fields = ('current_password', 'password1', 'password2',)

    def clean_currentpwd(self):
        current_password = self.cleaned_data.get("current_password")
        if current_password:
            raise forms.ValidationError("Incorrect password")
        return current_password

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2



# Student related forms
class StudentCreationForm(forms.Form):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER = [
        ('', '---------'),
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    email = forms.EmailField(max_length=255, widget=forms.EmailInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices=GENDER)
    date_of_birth = forms.DateField(label='Date of birth (DD/MM/YYYY)',
                                    widget=forms.DateInput(attrs={'type': 'date'}),
                                    required=True)
    grade_class = forms.ModelChoiceField(GradeClass.objects.all())
    phone_number = forms.CharField(label='Phone number', required=False)
    address_line_1 = forms.CharField(label='Address line 1', required=False)
    address_line_2 = forms.CharField(label='Address line 2 (optional)', required=False)
    postcode = forms.CharField(required=False)
    guardian_first_name = forms.CharField(required=False)
    guardian_last_name = forms.CharField(required=False)
    guardian_relationship = forms.CharField(required=False)
    guardian_phone_number = forms.CharField(required=False)
    notes = forms.CharField(label='Notes',
                            widget=forms.Textarea(attrs={'cols': '60', 'rows': '4'}),
                            required=False)

    class Meta:
        fields = ('email', 'first_name', 'last_name', 'date_of_birth',
                  'grade_class', 'phone_number', 'address_line_1', 'address_line_2', 'postcode',
                  'guardian_first_name', 'guardian_last_name', 'guardian_relationship', 'guardian_phone_number',
                  'notes')

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Account with this Email already exists.")
        else:
            return email


class StudentAccountUpdateForm(forms.ModelForm):
    is_active = forms.BooleanField(
        label='Active (deselect this if you want to revoke access for a user without deleting the account)',
        widget=forms.CheckboxInput
    )

    class Meta:
        model = Account
        fields = ('is_active', 'email', 'first_name', 'last_name', 'gender')


class StudentInfoUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Date of birth (DD/MM/YYYY)',
                                    widget=forms.DateInput(attrs={'type': 'date'}),
                                    required=True)
    notes = forms.CharField(label='Notes',
                            widget=forms.Textarea(attrs={'cols': '60', 'rows': '4'}),
                            required=False)

    class Meta:
        model = Student
        fields = ('date_of_birth', 'grade_class', 'phone_number', 'address_line_1', 'address_line_2', 'postcode',
                  'guardian_first_name', 'guardian_last_name', 'guardian_relationship', 'guardian_phone_number',
                  'notes')


# Teacher related forms
class TeacherCreationForm(forms.Form):
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER = [
        ('', '---------'),
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    teacher_grade_class_dictionary = {}
    for i in GradeClass.objects.all():
        teacher_grade_class_dictionary[i.id] = f'{i.grade_level}: {i.grade_class_name}'
    TEACHER_MULTIPLE_CHOICES = ((k, v) for k, v in zip(teacher_grade_class_dictionary.keys(),
                                                       teacher_grade_class_dictionary.values()))

    course_choices_dictionary = {'': '---------'}
    for i in Course.objects.all():
        course_choices_dictionary[i.id] = i.course_name
    COURSE_MULTIPLE_CHOICES = ((k, v) for k, v in zip(course_choices_dictionary.keys(),
                                                      course_choices_dictionary.values()))

    email = forms.EmailField(max_length=255, widget=forms.EmailInput)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    gender = forms.ChoiceField(choices=GENDER)
    date_of_birth = forms.DateField(label='Date of birth (DD/MM/YYYY)',
                                    widget=forms.DateInput(attrs={'type': 'date'}),
                                    required=True)
    grade_class = forms.MultipleChoiceField(choices=TEACHER_MULTIPLE_CHOICES)
    course = forms.ChoiceField(choices=COURSE_MULTIPLE_CHOICES)
    phone_number = forms.CharField(label='Phone number', required=False)
    address_line_1 = forms.CharField(label='Address line 1', required=False)
    address_line_2 = forms.CharField(label='Address line 2 (optional)', required=False)
    postcode = forms.CharField(required=False)

    class Meta:
        fields = ('email', 'first_name', 'last_name', 'date_of_birth',
                  'grade_class', 'course', 'phone_number', 'address_line_1', 'address_line_2', 'postcode',)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError("Account with this Email already exists.")
        else:
            return email

    def clean_course(self):
        course = self.cleaned_data.get('course')
        print("this is it", course)
        if not Course.objects.filter(id=course).exists():
            raise forms.ValidationError("Select a valid choice. That choice is not one of the available choices.")
        else:
            return course


class TeacherAccountUpdateForm(forms.ModelForm):
    is_active = forms.BooleanField(
        label='Active (deselect this if you want to revoke access for a user without deleting the account)',
        widget=forms.CheckboxInput
    )

    class Meta:
        model = Account
        fields = ('is_active', 'email', 'first_name', 'last_name', 'gender')


class TeacherInfoUpdateForm(forms.ModelForm):
    date_of_birth = forms.DateField(label='Date of birth (DD/MM/YYYY)',
                                    widget=forms.DateInput(attrs={'type': 'date'}),
                                    required=True)

    class Meta:
        model = Teacher
        fields = ('date_of_birth', 'grade_class', 'course', 'phone_number', 'address_line_1', 'address_line_2',
                  'postcode')


class CourseCreationForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('__all__')


class GradeLevelCreationForm(forms.ModelForm):
    class Meta:
        model = GradeLevel
        fields = ('__all__')


class GradeClassCreationForm(forms.ModelForm):
    class Meta:
        model = GradeClass
        fields = ('__all__')


class AcademicTermCreationForm(forms.ModelForm):
    academic_year = forms.DateField(label='Academic year (DD/MM/YYYY)',
                                    widget=forms.DateInput(attrs={'type': 'date'}),
                                    required=True)

    class Meta:
        model = AcademicTerm
        fields = ('academic_term_name', 'academic_term_multiplier', 'academic_year',)
