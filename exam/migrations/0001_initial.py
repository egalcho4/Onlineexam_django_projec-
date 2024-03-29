# Generated by Django 4.2 on 2023-04-09 18:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('descr', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=50)),
                ('question_number', models.PositiveIntegerField()),
                ('total_marks', models.PositiveIntegerField()),
                ('dep', models.IntegerField(null=True)),
                ('c_code', models.CharField(max_length=255, null=True)),
                ('year', models.IntegerField(null=True)),
                ('sem', models.IntegerField(null=True)),
                ('pre', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Password_manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=255, null=True)),
                ('last', models.CharField(max_length=255, null=True)),
                ('sid', models.CharField(max_length=255, null=True)),
                ('username', models.CharField(max_length=255, null=True)),
                ('pasword', models.CharField(max_length=255, null=True)),
                ('dep', models.IntegerField(null=True)),
                ('sem', models.IntegerField(null=True)),
                ('depa', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Permision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('perm', models.CharField(max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('date', models.DateTimeField(auto_now=True)),
                ('dep', models.IntegerField(null=True)),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marks', models.PositiveIntegerField()),
                ('question', models.CharField(max_length=600)),
                ('option1', models.CharField(max_length=200)),
                ('option2', models.CharField(max_length=200)),
                ('option3', models.CharField(max_length=200)),
                ('option4', models.CharField(max_length=200)),
                ('answer', models.CharField(choices=[('Option1', 'A'), ('Option2', 'B'), ('Option3', 'C'), ('Option4', 'D')], max_length=200)),
                ('dep', models.IntegerField(null=True)),
                ('examid', models.IntegerField(null=True)),
                ('image', models.ImageField(null=True, upload_to='question')),
                ('adby', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.course')),
            ],
        ),
        migrations.CreateModel(
            name='Departiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True)),
                ('colage_name', models.CharField(max_length=255, null=True)),
                ('adby', models.IntegerField(null=True)),
                ('head', models.IntegerField(null=True)),
                ('cl_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.collage')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='dp',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.departiment'),
        ),
    ]
