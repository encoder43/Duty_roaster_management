# Generated by Django 4.1.7 on 2023-05-17 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ShiftEase', '0011_editemployeeview'),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpdeskTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
            ],
        ),
    ]
