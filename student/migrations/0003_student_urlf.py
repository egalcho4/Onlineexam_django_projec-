# Generated by Django 4.2 on 2023-04-10 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_student_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='urlf',
            field=models.URLField(max_length=1000, null=True),
        ),
    ]
