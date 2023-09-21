from rest_framework import serializers
from .models import Posts
from comment.serializers import CommentSerializers

class PostSerializer(serializers.ModelSerializer):
    comment = CommentSerializers(many=True,read_only=True)

    class Meta:
        model = Posts
        fields = '__all__'
        read_only_fields = ('user',) 

    def create(self, validated_data):
        user = self.context.get('request').user
        post = Posts.objects.create(user=user, **validated_data)
        return post
