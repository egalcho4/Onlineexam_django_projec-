# Generated by Django 4.2.2 on 2023-07-03 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0045_alter_student_gen_alter_student_gender'),
        ('exam', '0024_result_tes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(null=True)),
                ('total', models.IntegerField(null=True)),
                ('exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.course')),
                ('student', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('test', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.test_hand')),
            ],
        ),
    ]
