# Generated by Django 3.1.3 on 2020-12-16 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_auto_20201216_1835'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='term',
            field=models.DateField(blank=True, default=None, null=True),
        ),
    ]
