# Generated by Django 3.1.3 on 2021-01-12 21:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0005_auto_20210111_2242'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChangeLog',
            new_name='Log',
        ),
    ]