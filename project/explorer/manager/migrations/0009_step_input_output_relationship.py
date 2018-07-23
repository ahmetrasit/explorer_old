# Generated by Django 2.0.7 on 2018-07-20 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_auto_20180720_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='step',
            name='input_output_relationship',
            field=models.CharField(choices=[('1 input file for 1 output', '1:1'), ('1 input file processed for many outputs', '1:*'), ('many input files for 1 output', '*>1'), ('many input files processed together for many outputs', '*>*'), ('Each input file corresponds to an individual output', '*:*')], default='1:1', max_length=128),
            preserve_default=False,
        ),
    ]