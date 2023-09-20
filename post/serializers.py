from rest_framework import serializers
from .models import Posts

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'
        read_only_fields = ('user',) 

    def create(self, validated_data):
        user = self.context.get('request').user
        post = Posts.objects.create(user=user, **validated_data)
        return post
