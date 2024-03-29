# Generated by Django 2.0.2 on 2018-07-30 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0015_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=2048)),
                ('protocol_id', models.IntegerField(blank=True, null=True)),
                ('step_id', models.IntegerField()),
                ('task_id', models.IntegerField(blank=True, null=True)),
                ('ancestry', models.TextField(blank=True, null=True)),
                ('created_by', models.CharField(max_length=256)),
                ('created_for', models.CharField(blank=True, max_length=256, null=True)),
                ('created_on', models.CharField(max_length=64)),
                ('folder_path', models.TextField()),
                ('access_list', models.TextField(blank=True, null=True)),
                ('major_types', models.TextField()),
                ('minor_types', models.TextField(blank=True, null=True)),
                ('source_file', models.TextField()),
                ('input_files', models.TextField()),
                ('output_files', models.TextField()),
                ('zipped', models.CharField(blank=True, max_length=64, null=True)),
                ('projects', models.TextField(blank=True, null=True)),
                ('size', models.TextField()),
                ('special', models.CharField(blank=True, max_length=64, null=True)),
                ('key_value', models.TextField()),
            ],
        ),
    ]
