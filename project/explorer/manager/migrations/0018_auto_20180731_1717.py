# Generated by Django 2.0.2 on 2018-07-31 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0017_auto_20180731_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datapoint',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='created_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
