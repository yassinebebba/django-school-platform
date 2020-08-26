from management.models import Account
from .models import Teacher, Exam
from django import forms
from digital_school import settings


class TeacherAccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('email',)


class TeacherInfoUpdateForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('phone_number',)


class ExamCreationForm(forms.ModelForm):

    teacher = forms.ChoiceField(widget=forms.HiddenInput, required=False)
    description = forms.CharField(label='Description',
                      widget=forms.Textarea(attrs={'cols': '60', 'rows': '4'}),
                      required=False)

    exam_creation_date = forms.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS,
                                             widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': 1}),
                                             required=True)
    exam_deadline = forms.DateTimeField(input_formats=settings.DATE_INPUT_FORMATS,
                                        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'step': 1}),
                                        required=True)


    
    '''
    teacher_class_choices = {}

    for i in Teacher.grade_class.all():
        teacher_class_choices[i.id] = i.grade_class_name
    TEACHER_CLASS_CHOICES = ((k, v) for k, v in zip(teacher_class_choices.keys(), teacher_class_choices.values()))
    grade_class = forms.ChoiceField(choices=TEACHER_CLASS_CHOICES)'''
    class Meta:
        model = Exam
        fields = (
            'grade_class', 'academic_term', 'academic_term', 'exam_type', 'exam_name', 'description',
            'exam_creation_date', 'exam_deadline', 'multiplier', 'full_mark',
        )
