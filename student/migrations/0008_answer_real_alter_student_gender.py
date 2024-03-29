# Generated by Django 4.2 on 2023-05-08 07:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0007_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='real',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('male', 'male'), ('female', 'female'), ('costom', 'costome')], max_length=255, null=True),
        ),
    ]
