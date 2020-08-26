from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, _user_has_perm, _user_has_module_perms
)
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import PermissionsMixin, Permission
import random
from django.utils import timezone


class AccountManager(BaseUserManager):
    def create_user(self, identifier, first_name, last_name, email, gender, password=None):
        # change the identifier to be a random ID for each category
        if not identifier:
            raise ValueError('Users must have an identifier.')
        if not first_name:
            raise ValueError('Users must have a first name.')
        if not last_name:
            raise ValueError('Users must have a last name.')
        if not email:
            raise ValueError('Users must have an email address.')
        if not gender:
            raise ValueError('Users must have a gender.')

        user = self.model(
            identifier=identifier,
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            gender=gender,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, first_name, last_name, email, gender, password=None):

        user = self.create_user(
            identifier=identifier,
            first_name=first_name,
            last_name=last_name,
            email=email,
            gender=gender,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    class Meta:
        permissions = [
            ("is_student", "Student"),
            ("is_teacher", "Teacher"),
        ]

    MALE = 'Male'
    FEMALE = 'Female'
    GENDER = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    identifier = models.CharField(max_length=20, unique=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=6, choices=GENDER)
    date_added = models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'identifier'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'gender']

    def __str__(self):
        return self.identifier

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def save(self, *args, **kwargs):
        self.first_name = self.first_name[0].upper() + self.first_name[1:]
        self.last_name = self.last_name[0].upper() + self.last_name[1:]
        if self.is_student:
            students_list = Account.objects.filter(is_student=True)
            last_student = students_list.order_by('identifier').last()
            try:
                Account.objects.get(identifier=self.identifier)
            except ObjectDoesNotExist:
                if last_student:
                    last_student_id = int(last_student.identifier)
                    self.identifier = str(last_student_id + 1)
                else:
                    self.identifier = '20000000'

        elif self.is_teacher:
            teachers_list = Account.objects.filter(is_teacher=True)
            last_teacher = teachers_list.order_by('identifier').last()
            try:
                Account.objects.get(identifier=self.identifier)
            except ObjectDoesNotExist:
                if last_teacher:
                    last_teacher_id = int(last_teacher.identifier[4:])
                    self.identifier = 'prof' + str(last_teacher_id + 1)
                else:
                    self.identifier = 'prof10000000'

        elif self.is_superuser:
            admin_list = Account.objects.filter(is_superuser=True)
            last_admin = admin_list.order_by('identifier').last()
            try:
                Account.objects.get(identifier=self.identifier)
            except ObjectDoesNotExist:
                if last_admin:
                    last_admin_id = int(last_admin.identifier[5:])
                    self.identifier = 'admin' + str(last_admin_id + 1)
                else:
                    self.identifier = 'admin10000000'
        super().save()

    @staticmethod
    def make_random_password(instance, length, allowed_chars):
        random_password = ""
        for _ in range(length):
            random_password += allowed_chars[random.randrange(len(allowed_chars))]
        instance.set_password(random_password)
        return instance


class GradeLevel(models.Model):
    grade_level_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return f'{self.grade_level_name}'


class Course(models.Model):
    course_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.course_name


class GradeClass(models.Model):
    grade_class_name = models.CharField(max_length=200, unique=True)
    grade_level = models.ForeignKey(GradeLevel, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course)

    class Meta:
        verbose_name_plural = 'Grade classes'

    def __str__(self):
        return f'{self.grade_level}: {self.grade_class_name}'


class CommonInfo(models.Model):
    address_line_1 = models.CharField(max_length=50, null=True, blank=True, name='address_line_1')
    address_line_2 = models.CharField(max_length=50, null=True, blank=True, name='address_line_2')
    postcode = models.CharField(max_length=8, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    date_of_birth = models.DateField(max_length=10)
    notes = models.TextField(null=True, blank=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AcademicTerm(models.Model):
    academic_term_name = models.CharField(max_length=100)
    academic_term_multiplier = models.FloatField()
    academic_year = models.DateField(max_length=10)

    def __str__(self):
        return f'{self.academic_term_name} (x{self.academic_term_multiplier})'
