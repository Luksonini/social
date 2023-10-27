from rest_framework import serializers
from . models import PostModel, CommentModel
from django.utils.html import urlize


class UrlizedCharField(serializers.CharField):

    def to_representation(self, value):
        return urlize_custom(value)
    
class PostModelSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M", required=False, read_only=True) 
    profile_image = serializers.ImageField(source='author.profile_picture', read_only=True)
    likes = serializers.IntegerField(source='post_likes.count', read_only=True)
    body = UrlizedCharField()

    class Meta:
        model = PostModel
        fields = ('id', 'author', 'author_username', 'body', 'created_at', 'profile_image', 'likes')
    

class CommentModelSerializer(serializers.ModelSerializer):
    """Serializer for the CommentModel."""
    author_username = serializers.CharField(source='user.username', read_only=True)
    profile_image = serializers.ImageField(source='user.profile_picture', read_only=True)
    class Meta:
        model = CommentModel
        fields = ['id', 'user', 'post', 'text', 'created_at', 'author_username', 'profile_image']

def urlize_custom(value):
    """Convert URLs in text to clickable links with target="_blank"."""
    value = urlize(value)
    return value.replace('<a ', '<a target="_blank" ')