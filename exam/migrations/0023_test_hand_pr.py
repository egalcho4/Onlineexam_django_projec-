# Generated by Django 4.2.2 on 2023-07-01 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0022_test_hand_question_tes'),
    ]

    operations = [
        migrations.AddField(
            model_name='test_hand',
            name='pr',
            field=models.IntegerField(null=True),
        ),
    ]
