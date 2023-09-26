from django.db import models
from post.models import Posts
from account.models import User

class Favorite(models.Model):
    posts = models.ForeignKey(Posts,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite = models.BooleanField(default=False)яяя