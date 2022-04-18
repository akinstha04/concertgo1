from django.contrib import admin
from .models import Profile, Post, Ticket, Comment, Wishlist

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(Wishlist)