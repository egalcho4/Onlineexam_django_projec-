# Generated by Django 4.2.2 on 2023-07-01 18:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0021_question_short'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test_hand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('tquest', models.IntegerField(null=True)),
                ('tmark', models.IntegerField(null=True)),
                ('pas', models.CharField(max_length=255, null=True)),
                ('course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.course')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.test_hand'),
        ),
    ]
