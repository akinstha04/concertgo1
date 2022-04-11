from audioop import reverse
from email.policy import default
from django.utils import timezone
from django.db import models
# from django.contrib.auth.models import User
from myapp.models import User
from django.urls import reverse
# from PIL import Image

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'profile_pics\default.jpg', upload_to='profile_pics')
    bio = models.TextField(default="hi")

    def __str__(self):
        return f'{self.user.username} Profile'

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 500 or img.width >500:
    #         output_size = (500, 500)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
    
class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts')
    detail = models.TextField(max_length=300)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.detail

    def get_absolute_url(self):
        return reverse('postDetail', kwargs={'pk': self.pk})