from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# from userprofile.views import PostListView, PostUpload, PostDetail

urlpatterns = [
    path('ticket_order/', views.orderTicket, name = "orderTicket"),
    
]
urlpatterns += staticfiles_urlpatterns()