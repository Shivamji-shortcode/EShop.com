# models/logo_config.py
from django.db import models

class LogoConfig(models.Model):
    # This stores your dynamic logo
    logo = models.ImageField(upload_to='products/')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Logo Configuration"
        verbose_name_plural = "Logo Configuration"

    def __str__(self):
        return f"Logo updated on {self.updated_at}"