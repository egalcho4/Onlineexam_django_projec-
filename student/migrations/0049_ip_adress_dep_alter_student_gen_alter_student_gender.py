# Generated by Django 4.2.2 on 2023-07-03 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0048_ip_adress_host_ip_adress_name_alter_student_gen_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ip_adress',
            name='dep',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gen',
            field=models.CharField(choices=[('female', 'female'), ('costom', 'costome'), ('male', 'male')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='gender',
            field=models.CharField(choices=[('female', 'female'), ('costom', 'costome'), ('male', 'male')], max_length=255, null=True),
        ),
    ]
