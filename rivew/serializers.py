from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Like

from rest_framework import serializers
from .models import Comment

class CommentSerializers(serializers.ModelSerializer):\

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',) 


    def create(self, validated_data):
        user = self.context.get('request').user
        comment = self.Meta.model(author=user, **validated_data)
        comment.save()
        return comment



class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    post = ReadOnlyField(source='post.id')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)
