from django.db import models
from account.models import User

class Category(models.Model):
    name = models.CharField(max_length=25, unique=True)

class Posts(models.Model):
    title = models.CharField(max_length=50)
    file_video = models.FileField(upload_to='videos/', blank=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category)
    data_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')

