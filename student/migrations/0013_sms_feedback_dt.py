# Generated by Django 4.2.1 on 2023-05-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0012_sms_feedback_seen_alter_student_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='sms_feedback',
            name='dt',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
