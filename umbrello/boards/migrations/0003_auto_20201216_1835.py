# Generated by Django 3.1.3 on 2020-12-16 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0002_card_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='list',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
