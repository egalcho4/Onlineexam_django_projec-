# Generated by Django 4.2.10 on 2024-03-24 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0049_ip_adress_dep_alter_student_gen_alter_student_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='gen',
            field=models.CharField(choices=[('female', 'female'), ('male', 'male'), ('costom', 'costome')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('female', 'female'), ('male', 'male'), ('costom', 'costome')], max_length=255, null=True),
        ),
    ]