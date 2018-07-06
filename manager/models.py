from django.db import models


class MainConfiguration(models.Model):
    team_name = models.CharField(max_length=32)
    intro_message = models.CharField(max_length=256)
    cpu_ratio = models.DecimalField(max_digits=3, decimal_places=2)
    ram_ratio = models.DecimalField(max_digits=3, decimal_places=2)
    key_value = models.TextField()
    created_on = models.DateTimeField(auto_now=True)
