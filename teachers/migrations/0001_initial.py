# Generated by Django 3.0.1 on 2020-08-27 01:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(blank=True, max_length=50, null=True)),
                ('address_line_2', models.CharField(blank=True, max_length=50, null=True)),
                ('postcode', models.CharField(blank=True, max_length=8, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('date_of_birth', models.DateField(max_length=10)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('account', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='management.Course')),
                ('grade_class', models.ManyToManyField(to='management.GradeClass')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam_type', models.CharField(default='Exam', max_length=4)),
                ('exam_name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, max_length=500, null=True)),
                ('exam_creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('exam_deadline', models.DateTimeField()),
                ('multiplier', models.FloatField(max_length=3)),
                ('full_mark', models.IntegerField(default=20)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('academic_term', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.AcademicTerm')),
                ('grade_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='management.GradeClass')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teachers.Teacher')),
            ],
        ),
    ]