# Generated by Django 4.2.2 on 2023-06-28 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0033_alter_student_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('costom', 'costome'), ('male', 'male'), ('female', 'female')], max_length=255, null=True),
        ),
    ]
