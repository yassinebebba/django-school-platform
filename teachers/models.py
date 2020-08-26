from django.db import models
from management.models import (
    Account, CommonInfo, GradeClass, Course, AcademicTerm
)
from django.utils import timezone

class Teacher(CommonInfo, models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    grade_class = models.ManyToManyField(GradeClass)
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    notes = None

    def __str__(self):
        return self.account.__str__()

class Exam(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)  # auto
    grade_class = models.ForeignKey(GradeClass, on_delete=models.CASCADE, null=True, blank=True)
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)  # manual
    exam_type = models.CharField(max_length=4, default='Exam')  # auto
    exam_name = models.CharField(max_length=255)  # manual
    description = models.TextField(max_length=500, blank=True, null=True)  # manual
    exam_creation_date = models.DateTimeField(default=timezone.now)  # auto
    exam_deadline = models.DateTimeField()  # manual
    multiplier = models.FloatField(max_length=3)  # manual
    full_mark = models.IntegerField(default=20)  # manual
    modified = models.DateTimeField(auto_now=True)  # auto

    def __str__(self):
        return self.teacher.__str__()