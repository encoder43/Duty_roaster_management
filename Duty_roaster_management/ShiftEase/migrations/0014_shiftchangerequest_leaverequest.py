# Generated by Django 4.1.7 on 2023-05-17 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftEase', '0013_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftChangeRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_id', models.IntegerField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='LeaveRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ShiftEase.employeedetail')),
            ],
        ),
    ]
