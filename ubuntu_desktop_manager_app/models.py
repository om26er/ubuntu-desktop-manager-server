from django.db import models

from simple_login.models import BaseUser


class User(BaseUser):
    account_activation_sms_otp = None
    password_reset_sms_otp = None


class Device(models.Model):
    user = models.ForeignKey(User, related_name='user')
    device_id = models.CharField(max_length=255, blank=False, unique=True)
