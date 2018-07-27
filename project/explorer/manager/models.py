from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    CHOICES = ((role, role) for role in ('bioinformatician', 'scientist', 'intern', 'other', 'boss'))

    created_on = models.DateTimeField(auto_now=True)
    role = models.CharField(choices=CHOICES, max_length=128, default=None, blank=True, null=True)
    credit = models.PositiveSmallIntegerField( default=None, blank=True, null=True)
    special = models.CharField(max_length=128, default=None, blank=True, null=True)
    score = models.CharField(max_length=128, default=None, blank=True, null=True)
    key_value = models.TextField(default=None, blank=True, null=True)


class MainConfiguration(models.Model):
    team_name = models.CharField(max_length=64)
    intro_message = models.CharField(max_length=256)
    cpu_ratio = models.DecimalField(max_digits=3, decimal_places=2)
    ram_ratio = models.DecimalField(max_digits=3, decimal_places=2)
    key_value = models.TextField()
    created_on = models.DateTimeField(auto_now=True)


class MajorDataCategory(models.Model):
    category = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=256)
    sample_schema = models.CharField(max_length=256, blank=True, null=True)
    special = models.CharField(max_length=128, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)


class Step(models.Model):
    USERS = ((user,user) for user in CustomUser.objects.values_list('username', flat=True) if user != 'admin')
    DATA_CATEGORIES = ((category,category) for category in MajorDataCategory.objects.values_list('category', flat=True))
    ACCESS = ((access, access) for access in ('public', 'private'))
    STATUS = ((status, status) for status in ('tested', 'experimental'))
    SPECIAL = ((special, special) for special in ('regular', 'upload', 'other'))
    NO_OF = ((no_of, description) for description, no_of in (('one output', 'one'), ('many outputs of the same kind', 'many')))
    RELATIONSHIP = ((relation, description) for description, relation in (('1 input file for 1 output', '1:1'), ('1 input file processed for many outputs', '1:*'), ('many input files for 1 output', '*>1'), ('many input files processed together for many outputs', '*>*'), ('Each input file corresponds to an individual output', '*:*')))

    short_name = models.CharField(max_length=64, unique=True)
    no_of_outputs = models.CharField(max_length=64, choices=NO_OF)
    output_major_data_category = models.CharField(max_length=128, choices=DATA_CATEGORIES)
    input_output_relationship = models.CharField(max_length=128, choices=RELATIONSHIP)
    sample_schema = models.CharField(max_length=256, blank=True, null=True)
    created_for = models.CharField(max_length=256, choices=USERS, blank=True, null=True)
    access_list = models.CharField(max_length=2048, choices=ACCESS)
    description = models.CharField(max_length=2048)
    status = models.CharField(max_length=256, choices=STATUS)
    special = models.CharField(max_length=256, choices=SPECIAL)
    script = models.TextField()

    created_by = models.CharField(max_length=256)
    subfolder_path = models.CharField(max_length=256)
    dependencies = models.TextField()
    input_major_data_category = models.CharField(max_length=128)
    minor_data = models.CharField(max_length=256)
    score = models.CharField(max_length=256)
    key_value = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now=True)


class Reference(models.Model):
    short_name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=2048)
    reference_type = models.CharField(max_length=64)
    placeholder = models.CharField(max_length=256)

    script = models.TextField()
    completed = models.CharField(max_length=256)
    special = models.CharField(max_length=256)
    created_by = models.CharField(max_length=256)
    subfolder_path = models.CharField(max_length=256)
    dependencies = models.TextField()
    score = models.CharField(max_length=256)
    key_value = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now=True)


class Task(models.Model):
    step_id = models.IntegerField()
    protocol_id = models.IntegerField()
    process_id = models.IntegerField()
    retry_of = models.IntegerField(blank=True, null=True)
    depends_on = models.IntegerField(blank=True, null=True)

    input_file = models.TextField()
    script = models.TextField()
    folder_path = models.TextField()
    major_types = models.TextField()
    minor_types = models.TextField(blank=True, null=True)
    save_outputs_zipped = models.CharField(max_length=64)

    created_by = models.CharField(max_length=256)
    created_for = models.CharField(max_length=256, blank=True, null=True)
    created_on = models.CharField(max_length=64)
    started_on = models.CharField(max_length=64, blank=True, null=True)
    finished_on = models.CharField(max_length=64, blank=True, null=True)
    is_last = models.CharField(max_length=64)
    status = models.CharField(max_length=64)
    finished_status = models.CharField(max_length=64, blank=True, null=True)
    retries_left = models.IntegerField()

    special = models.CharField(max_length=64, blank=True, null=True)
    key_value = models.CharField(max_length=64, blank=True, null=True)
