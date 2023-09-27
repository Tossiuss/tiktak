from django.db import models
from account.models import User


class Subscription(models.Model):
    friend_email = models.EmailField()  # Поле для хранения email друга
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_subscriptions')

    def __str__(self):
        return self.friend_email
    