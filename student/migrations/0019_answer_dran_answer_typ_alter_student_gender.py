# Generated by Django 4.2.1 on 2023-05-16 17:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0018_alter_student_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='dran',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AddField(
            model_name='answer',
            name='typ',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('female', 'female'), ('male', 'male'), ('costom', 'costome')], max_length=255, null=True),
        ),
    ]
