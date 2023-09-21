from rest_framework import serializers
from .models import Comment

class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author',) 


    def create(self, validated_data):
        user = self.context.get('request').user
        post = Comment.objects.create(author=user, **validated_data)
        return post
    