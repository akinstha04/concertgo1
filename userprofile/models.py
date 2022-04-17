from audioop import reverse
from email.policy import default
from tkinter import CASCADE
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
    following = models.ManyToManyField(User, related_name='following', blank=True)
    followers = models.ManyToManyField(User,related_name='followers', blank=True)

    def profile_posts(self):
        return self.post_set.all()
    
    def profile_tickets(self):
        return self.ticket_set.all()

    def total_followers(self):
        return self.followers.count()
    def total_following(self):
        return self.following.count()

    def __str__(self):
        # return f'{self.user.username} Profile'
        return str(self.user.username)

    # def save(self):
    #     super().save()

    #     img = Image.open(self.image.path)

    #     if img.height > 500 or img.width >500:
    #         output_size = (500, 500)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path)
    
class Post(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts')
    detail = models.TextField(max_length=300)
    date_posted = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(Profile, related_name="posts")

    def __str__(self):
        return self.detail

    def get_absolute_url(self):
        return reverse('postDetail', kwargs={'pk': self.pk})
    
    def total_likes(self):
        return self.likes.count()

class Ticket(models.Model):
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    detail = models.TextField(max_length=200)
    date = models.DateField()
    ex_date = models.DateTimeField()    #the time after which the ticket cannot be purchased.
    price = models.FloatField(max_length=255)
    image = models.ImageField(default = 'ticket_pics\default.jpg',upload_to='ticket_pics')
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ticketDetail', kwargs={'pk': self.pk})

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return '%s - %s' % (self.body, self.user)
    