# Generated by Django 4.2.13 on 2024-08-30 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='roll_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='section',
            field=models.CharField(max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='student_class',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
