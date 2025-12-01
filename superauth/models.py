from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    totp_secret = models.CharField(max_length=32, null=True, blank=True)
    verify_code = models.CharField(max_length=6, null=True, blank=True)
    verify_code_expire_at = models.DateTimeField(null=True, blank=True)
    is_verify = models.BooleanField(default=False)
    is_default_change = models.BooleanField(default=False)

    def __str__(self):
        return self.get_full_name() or self.username  
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']


