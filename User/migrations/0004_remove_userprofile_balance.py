# Generated by Django 5.1.7 on 2025-03-10 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0003_userprofile_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='balance',
        ),
    ]
