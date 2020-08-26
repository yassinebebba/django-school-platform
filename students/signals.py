from django.db.models.signals import post_save
from teachers.models import Exam
from django.dispatch import receiver
from .models import ExamGrade


@receiver(post_save, sender=Exam)
def create_exam_grade(sender, instance, created, **kwargs):
    if created:
        # grade_class.get(id=1).student_set.all()
        exam_grade_class = instance.grade_class
        related_students = exam_grade_class.student_set.all()
        # for loop students
        for student in related_students:
            ExamGrade.objects.create(
                student=student,
                exam=instance,
                exam_course=instance.teacher.course.course_name,
            )


# this signals has to have its own deletion instructions
'''@receiver(post_save, sender=Exam)
def create_exam_grade(sender, instance, created, **kwargs):
    if created:
        # grade_class.get(id=1).student_set.all()
        exam_grade_class = instance.grade_class
        related_students = exam_grade_class.student_set.all()
        teacher = instance.teacher
        grade_class = instance.grade_class
        academic_term = instance.academic_term
        exam_type = instance.exam_type
        exam_course = instance.teacher.course.course_name
        exam_name = instance.exam_name
        exam_creation_date = instance.exam_creation_date
        exam_deadline = instance.exam_deadline
        multiplier = instance.multiplier
        full_mark = instance.full_mark
        grade_result = instance.grade_result
        # for loop students
        for student in related_students:
            ExamGrade.objects.create(
                student=student,
                teacher=teacher,
                grade_class=grade_class,
                academic_term=academic_term,
                exam_type=exam_type,
                exam_course=exam_course,
                exam_name=exam_name,
                exam_creation_date=exam_creation_date,
                exam_deadline=exam_deadline,
                multiplier=multiplier,
                full_mark=full_mark,
                grade_result=grade_result,
            )
'''

'''
@receiver(post_save, sender=Exam)
def save_exam_grade(sender, instance, **kwargs):
    instance.save()
'''
