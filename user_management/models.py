from django.db import models
from .utils import DeviceTypes


class BaseModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class User(BaseModel):
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    is_delete = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    logged_out = models.BooleanField(default=False)
    last_login = models.DateTimeField(auto_now=True)
    last_device = models.IntegerField(
        choices=DeviceTypes.choices, null=True, blank=True
    )