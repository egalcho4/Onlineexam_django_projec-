# Generated by Django 4.2.2 on 2023-06-25 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0009_alter_collage_name_alter_course_c_code_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='lct',
            field=models.IntegerField(null=True),
        ),
    ]
