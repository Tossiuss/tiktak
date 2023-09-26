# views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer
from post.models import Posts

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'])
    def toggle_like(self, request, pk=None):
        post = Posts.objects.get(pk=pk)  # Получаем объект поста по переданному pk
        user = request.user
        try:
            like = Like.objects.get(post=post, author=user)
            like.like = not like.like  # Переключаем значение поля like
            like.save()
            message = 'unliked' if not like.like else 'liked'
        except Like.DoesNotExist:
            Like.objects.create(post=post, author=user, like=True)
            message = 'liked'
        return Response({"message": message}, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)