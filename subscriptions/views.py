from rest_framework import generics
from rest_framework import permissions
from .models import Subscription
from .serializers import SubscriptionSerializer
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import serializers

User = get_user_model()

class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        friend_email = serializer.validated_data.get('friend_email')  # Получаем email друга

        try:
            friend = User.objects.get(email=friend_email)
        except User.DoesNotExist:
            return Response({"detail": "Пользователь с указанным email не найден."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверим, что пользователь не пытается подписаться на самого себя
        if friend == user:
            return Response({"detail": "Вы не можете подписаться на самого себя."}, status=status.HTTP_400_BAD_REQUEST)

        # Проверим, не существует ли уже подписки на этого друга
        existing_subscription = Subscription.objects.filter(friend_email=friend_email, follower=user)
        if existing_subscription.exists():
            return Response({"detail": "Вы уже подписаны на этого друга."}, status=status.HTTP_400_BAD_REQUEST)

        # Создаем подписку
        subscription = Subscription(friend_email=friend_email, follower=user)
        subscription.save()

        return Response({"detail": "Подписка успешно создана."}, status=status.HTTP_201_CREATED)
    


class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Получите список подписок для текущего пользователя
        queryset = Subscription.objects.filter(follower=user)
        return queryset
    

    

class SubscriptionDeleteView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        friend_email = self.kwargs.get('friend_email')  # Получаем email друга из URL
        user = self.request.user  # Получаем текущего аутентифицированного пользователя
        # Попробуем найти подписку на друга
        try:
            subscription = Subscription.objects.get(friend_email=friend_email, follower=user)
        except Subscription.DoesNotExist:
            raise serializers.ValidationError("Подписка на этого друга не найдена.")
        return subscription

    def perform_destroy(self, instance):
        # Удаляем подписку
        instance.delete()

        # Отвечаем, что подписка успешно удалена
        return Response({"detail": "Подписка успешно удалена."}, status=status.HTTP_204_NO_CONTENT)