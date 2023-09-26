from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions



class IsCommentAuthorOrPostAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:
            return True

        if obj.posts.user == request.user:
            return True

        return False


class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsCommentAuthorOrPostAuthorOrReadOnly]
    http_method_names = ['get', 'post', 'delete']


    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"user": ["Пользователь не аутентифицирован"]}, status=status.HTTP_401_UNAUTHORIZED)

        # user = request.user

        serializer = CommentSerializers(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
