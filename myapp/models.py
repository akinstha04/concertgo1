from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

from django.utils import timezone
from django.urls import reverse
# Create your models here.



class User(AbstractUser):
    is_manager = models.BooleanField('Is manager', default=False)
    # is_customer = models.BooleanField('Is customer', default=True)



class Ticket(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    price = models.CharField(max_length=255)
    image = models.ImageField(upload_to='ticket_pic')
    sale = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name