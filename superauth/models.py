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


class OTPRecord(models.Model):

    identity = models.CharField(max_length=255,help_text="Email or phone number") 
    otp = models.CharField(max_length=8)   
    purpose = models.CharField(max_length=50,default="login",
        choices=[
            ("login", "Login OTP"),
            ("register", "Registration"),
            ("password_reset", "Password Reset"),
            ("2fa_setup", "2FA Setup"),
            ("backup", "Backup Code"),
        ],
        help_text="Is OTP ka use kya hai?"
    )    
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    attempts = models.PositiveIntegerField(default=0)
    
    class Meta:
        indexes = [models.Index(fields=['identity', 'purpose']),  models.Index(fields=['expires_at']),]
        ordering = ['-created_at']
        verbose_name = "OTP Record"
        verbose_name_plural = "OTP Records"

    def __str__(self):
        return f"{self.identity} | {self.otp} ({self.purpose}) {'[USED]' if self.is_used else ''}"

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def mark_as_used(self):
        self.is_used = True
        self.save(update_fields=['is_used'])