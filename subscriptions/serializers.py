from rest_framework import serializers
from .models import Subscription
from django.contrib.auth import get_user_model

User = get_user_model()

class SubscriptionSerializer(serializers.ModelSerializer):
    friend_email = serializers.EmailField()  # Добавляем поле для email друга

    class Meta:
        model = Subscription
        fields = ['friend_email']  # Оставляем только поле friend_email

    def create(self, validated_data):
        follower = self.context.get('request').user
        friend_email = validated_data.get('friend_email')

        # Попробуем найти пользователя по email друга
        try:
            friend = User.objects.get(email=friend_email)
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь с указанным email не найден.")

        # Проверим, что пользователь не пытается подписаться на самого себя
        if friend == follower:
            raise serializers.ValidationError("Вы не можете подписаться на самого себя.")

        # Проверим, не существует ли уже подписки на этого друга
        existing_subscription = Subscription.objects.filter(friend_email=friend_email, follower=follower)
        if existing_subscription.exists():
            raise serializers.ValidationError("Вы уже подписаны на этого друга.")

        # Создаем подписку
        subscription = Subscription(friend_email=friend_email, follower=follower)
        subscription.save()

        return subscription
    

def delete(self):
    follower = self.context.get('request').user
    friend_email = self.validated_data.get('friend_email')

    # Попробуем найти подписку на друга
    try:
        subscription = Subscription.objects.get(friend_email=friend_email, follower=follower)
    except Subscription.DoesNotExist:
        raise serializers.ValidationError("Подписка на этого друга не найдена.")

    # Удаляем подписку
    subscription.delete()

    # Возвращаем сообщение об успешном удалении или None
    return {"message": "Подписка успешно удалена."}




