from rest_framework import serializers
from post.models import Posts
from rivew.serializers import CommentSerializers
from rivew.serializers import LikeSerializer

class PostSerializer(serializers.ModelSerializer):
    likes = LikeSerializer(many=True, read_only=True)

    class Meta:
        model = Posts
        fields = '__all__'
        read_only_fields = ('user',)


    def create(self, validated_data):
        user = self.context.get('request').user
        post = Posts.objects.create(user=user, **validated_data)
        return post


    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr['comment'] = CommentSerializers(instance.comment.all(), many=True).data
        return repr