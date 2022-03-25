from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver

# Create your models here.



# class User(AbstractUser):
#     is_manager = models.BooleanField(default=False)

# class manager(models.Model):
#     user = models.OneToOneField(User, ondelete = models.CASCADE, primary_key=True)
#     address = models.CharField(max_length=80)

#     def __str__(self):
#         return self.user.username




# 
# class User(AbstractUser):
#     is_appuser = models.BooleanField(default=False)
#     is_manager = models.BooleanField(default=False)

# class Appuser(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user.is_appuser = True
#     uid = models.AutoField(unique=True, primary_key=True) #user identification

# class Manager(models.Model):
#     mid = models.AutoField(primary_key=True) #unique manager identification number
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     user.is_manager = True
#     location = models.CharField(max_length=20)
#     # days_available = models.DateTimeField(null=True)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.is_patient:
#             Patient.objects.create(user=instance)
#         elif instance.is_doctor:
#             Doctor.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     if instance.is_patient:
#         instance.patient.save()
#     elif instance.is_doctor:
#         instance.doctor.save()