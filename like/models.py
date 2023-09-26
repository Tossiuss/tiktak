from django.db import models
from post.models import Posts
from account.models import User


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='likes')
    like = models.BooleanField(default=False)



    def __str__(self):
        return f"Like by {self.author.name} on {self.post.title}"
