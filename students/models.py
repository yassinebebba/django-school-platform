from django.db import models
from management.models import (
    Account, CommonInfo, GradeClass, AcademicTerm
)
from django.utils import timezone
from teachers.models import Teacher, Exam


class Student(CommonInfo, models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    grade_class = models.ForeignKey(GradeClass, on_delete=models.DO_NOTHING, null=True, blank=True)
    guardian_first_name = models.CharField(max_length=30, null=True, blank=True)
    guardian_last_name = models.CharField(max_length=30, null=True, blank=True)
    guardian_relationship = models.CharField(max_length=50, null=True, blank=True)
    guardian_phone_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.account.__str__()


# fix exam deletion with a signal
# this is to minimise processing and database strain
class ExamGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # auto
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)  # auto
    exam_course = models.CharField(max_length=100)  # auto
    grade_result = models.FloatField(max_length=3, null=True, blank=True)  # manual
    feedback = models.TextField(max_length=300, null=True, blank=True)  # manual
    modified = models.DateTimeField(auto_now=True)  # auto

    def __str__(self):
        return self.exam.exam_name


'''
# fix exam deletion with a signal
class ExamGrade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)  # auto
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # auto
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)  # manual
    grade_class = models.ForeignKey(GradeClass, on_delete=models.CASCADE, null=True, blank=True)
    exam_type = models.CharField(max_length=4, default='Exam')  # auto
    exam_course = models.CharField(max_length=100)  # auto
    exam_name = models.CharField(max_length=255)  # manual
    exam_creation_date = models.DateTimeField(default=timezone.now)  # auto
    exam_deadline = models.DateTimeField()  # manual
    multiplier = models.FloatField(max_length=3)  # manual
    full_mark = models.IntegerField(default=20)  # manual
    grade_result = models.FloatField(max_length=3, null=True, blank=True)  # manual
    feedback = models.TextField(max_length=300, null=True, blank=True)  # manual
    modified = models.DateTimeField(auto_now=True)  # auto

    def __str__(self):
        return self.student.__str__()
'''