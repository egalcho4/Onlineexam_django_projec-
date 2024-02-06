# Generated by Django 4.2.2 on 2023-06-28 12:35

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0012_year_now'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('datr', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200), blank=True, null=True, size=None)),
                ('qid', models.IntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.tables'),
        ),
    ]
