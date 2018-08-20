# Generated by Django 2.0.2 on 2018-08-20 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0025_auto_20180817_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reference',
            name='completed',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='dependencies',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='key_value',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='placeholder',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='score',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='script',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reference',
            name='special',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]