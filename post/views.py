from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from .serializers import PostSerializer
from .models import Posts
from django.contrib.auth import get_user_model

User = get_user_model()


class PostView(viewsets.ModelViewSet):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    http_method_names = ['get', 'post', 'delete', 'retrieve']

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"user": ["Пользователь не аутентифицирован"]}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = PostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
