from rest_framework import serializers
from .models import Posts
from rivew.serializers import CommentSerializers
from rivew.serializers import LikeSerializer
from account.models import User

class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)


    class Meta:
        model = Posts, User
        fields = ('__all__', 'name', 'avatar')
        read_only_fields = ('user') 

    def create(self, validated_data):
        user = self.context.get('request').user
        post = Posts.objects.create(user=user, **validated_data)
        return post
