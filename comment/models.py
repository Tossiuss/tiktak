from django.db import models
from post.models import Posts
from account.models import User


class Comment(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment')
    posts = models.ForeignKey(Posts,on_delete=models.CASCADE,related_name='comment')
    comment = models.CharField(max_length=255)
    data_create = models.DateTimeField(auto_now_add=True)


    


