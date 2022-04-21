from django.db import models
from userprofile.models import Profile, Ticket
from audioop import reverse
from tkinter import CASCADE
from django.utils import timezone
from django.urls import reverse
# Create your models here.


class Order(models.Model):
    ticket = models.ForeignKey(Ticket, related_name="ticket", on_delete=models.CASCADE)
    buyer = models.ForeignKey(Profile,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    date_purchased = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s - %s' % (self.buyer, self.ticket, self.quantity)