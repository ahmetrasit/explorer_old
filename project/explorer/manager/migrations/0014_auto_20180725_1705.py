# Generated by Django 2.0.7 on 2018-07-25 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0013_auto_20180724_2218'),
    ]

    operations = [
        migrations.AddField(
            model_name='majordatacategory',
            name='sample_schema',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='majordatacategory',
            name='special',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='step',
            name='no_of_outputs',
            field=models.CharField(choices=[('one', 'one output'), ('many', 'many outputs of the same kind')], max_length=64),
        ),
    ]
