from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

from django.utils import timezone
from django.urls import reverse
# Create your models here.



class User(AbstractUser):
    is_manager = models.BooleanField('Is manager', default=False)
    # is_customer = models.BooleanField('Is customer', default=True)

