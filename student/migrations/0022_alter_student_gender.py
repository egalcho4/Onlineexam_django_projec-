# Generated by Django 4.2.1 on 2023-06-07 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_alter_student_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('female', 'female'), ('costom', 'costome'), ('male', 'male')], max_length=255, null=True),
        ),
    ]
