# Generated by Django 4.2.1 on 2023-05-09 11:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0009_alter_student_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sms_feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.IntegerField(null=True)),
                ('msg', models.TextField(null=True)),
                ('replay', models.TextField(null=True)),
                ('dep', models.IntegerField(null=True)),
                ('status', models.CharField(max_length=255, null=True)),
                ('rec', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
