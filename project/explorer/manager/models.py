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
    special = models.CharField(max_length=32, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)


class Step(models.Model):
    USERS = ((user,user) for user in CustomUser.objects.values_list('username', flat=True) if user != 'admin')
    ACCESS = ((access, access) for access in ('public', 'private'))
    STATUS = ((status, status) for status in ('tested', 'experimental'))
    SPECIAL = ((special, special) for special in ('regular', 'upload', 'public', 'other'))

    short_name = models.CharField(max_length=64, unique=True)
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
    output_major_data_category = models.CharField(max_length=128)
    minor_data = models.CharField(max_length=256)
    one_or_many_input_files = models.CharField(max_length=32)
    score = models.CharField(max_length=256)
    key_value = models.CharField(max_length=256)
    created_on = models.DateTimeField(auto_now=True)
