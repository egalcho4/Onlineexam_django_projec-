# Generated by Django 4.2.2 on 2023-06-28 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0014_remove_tables_datr_remove_tables_qid_table_data_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table_data',
            name='table',
        ),
        migrations.AddField(
            model_name='tables',
            name='dt',
            field=models.ManyToManyField(to='exam.table_data'),
        ),
        migrations.AlterField(
            model_name='question',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='exam.tables'),
        ),
    ]
