from django.db import models
from account.models import User

class Posts(models.Model):
    title = models.CharField(max_length=30)
    file_video = models.FileField(upload_to='videos/')
    description = models.TextField()
    categories = models.CharField(blank=False)
    data_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='post')

