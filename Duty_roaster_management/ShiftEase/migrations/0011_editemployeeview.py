# Generated by Django 4.1.7 on 2023-05-17 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftEase', '0010_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditEmployeeView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]