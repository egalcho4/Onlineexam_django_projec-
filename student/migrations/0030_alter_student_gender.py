# Generated by Django 4.2.2 on 2023-06-28 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0029_alter_student_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('costom', 'costome'), ('female', 'female')], max_length=255, null=True),
        ),
    ]
