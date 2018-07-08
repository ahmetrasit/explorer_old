from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    CHOICES = (('bioinformatician', 'bioinformatician'),('scientist', 'scientist'), ('intern', 'intern'), ('other', 'other'), ('boss', 'boss'))

    created_on = models.DateTimeField(auto_now=True)
    role = models.CharField(choices=CHOICES, max_length=128, default=None, blank=True, null=True)
    credit = models.PositiveSmallIntegerField( default=None, blank=True, null=True)
    special = models.CharField(max_length=128, default=None, blank=True, null=True)
    score = models.CharField(max_length=128, default=None, blank=True, null=True)
    key_value = models.TextField(default=None, blank=True, null=True)


class MainConfiguration(models.Model):
    team_name = models.CharField(max_length=64)
    intro_message = models.CharField(max_length=255)
    cpu_ratio = models.DecimalField(max_digits=3, decimal_places=2)
    ram_ratio = models.DecimalField(max_digits=3, decimal_places=2)
    key_value = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
