# Generated by Django 4.1.7 on 2023-04-09 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftEase', '0005_delete_supervisordetail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeedetail',
            name='empcode',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
