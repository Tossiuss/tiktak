from rest_framework.serializers import ModelSerializer, ReadOnlyField
from .models import Like

class LikeSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.email')
    post = ReadOnlyField(source='post.id')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        return self.Meta.model.objects.create(author=user, **validated_data)
