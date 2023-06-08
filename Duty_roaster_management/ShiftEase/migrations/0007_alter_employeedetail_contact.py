# Generated by Django 4.1.7 on 2023-04-09 09:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftEase', '0006_alter_employeedetail_empcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedetail',
            name='contact',
            field=models.CharField(max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator('^\\d{1,10}$')]),
        ),
    ]
