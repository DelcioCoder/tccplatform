# Generated by Django 5.1.7 on 2025-03-23 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connections', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='connectionrequest',
            old_name='create_at',
            new_name='created_at',
        ),
    ]
